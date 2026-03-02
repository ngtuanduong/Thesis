import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../prisma/prisma.service';
import { CreateSubmissionDto } from './dto/create-submission.dto';
import { CodeExecutionService } from './code-execution.service';
import { AdaptiveService } from '../adaptive/adaptive.service';
import { SubmissionStatus } from '@prisma/client';

@Injectable()
export class SubmissionsService {
  private readonly logger = new Logger(SubmissionsService.name);
  private aiServiceUrl: string;
  private aiServiceKey: string;

  constructor(
    private prisma: PrismaService,
    private codeExecutionService: CodeExecutionService,
    private configService: ConfigService,
    private adaptiveService: AdaptiveService,
  ) {
    this.aiServiceUrl = this.configService.get<string>('AI_SERVICE_URL') || 'http://localhost:8000';
    this.aiServiceKey = this.configService.get<string>('AI_SERVICE_KEY') || 'dev-secret-key';
  }

  async create(dto: CreateSubmissionDto, userId: string) {
    // Create submission with PENDING status
    const submission = await this.prisma.submission.create({
      data: { ...dto, userId, status: SubmissionStatus.PENDING },
    });

    // Execute code asynchronously
    this.executeSubmission(submission.id, dto.problemId, dto.code, dto.language).catch(
      (error) => {
        console.error('Failed to execute submission:', error);
      },
    );

    return submission;
  }

  private async executeSubmission(
    submissionId: string,
    problemId: string,
    code: string,
    language: string,
  ) {
    try {
      // Update status to RUNNING
      await this.prisma.submission.update({
        where: { id: submissionId },
        data: { status: SubmissionStatus.RUNNING },
      });

      // Get test cases
      const testCases = await this.prisma.testCase.findMany({
        where: { problemId },
        select: { input: true, expected: true },
      });

      if (testCases.length === 0) {
        await this.prisma.submission.update({
          where: { id: submissionId },
          data: {
            status: SubmissionStatus.RUNTIME_ERROR,
            output: 'No test cases found for this problem',
          },
        });
        return;
      }

      // Execute code
      const result = await this.codeExecutionService.executeCode(
        code,
        language,
        testCases,
      );

      // Update submission with results
      const updatedSubmission = await this.prisma.submission.update({
        where: { id: submissionId },
        data: {
          status: result.status,
          output: result.output || result.error || '',
          runtime: result.runtime || null,
          memory: result.memory || null,
        },
      });

      // If submission was accepted, update user's skill profile
      if (result.status === SubmissionStatus.ACCEPTED) {
        await this.updateUserSkills(updatedSubmission.userId).catch((error) => {
          this.logger.error(`Failed to update user skills: ${error.message}`);
        });
      }

      // Update adaptive learning layers (BKT, Elo, MAB, FSRS)
      if (
        result.status === SubmissionStatus.ACCEPTED ||
        result.status === SubmissionStatus.WRONG_ANSWER
      ) {
        const attemptCount = await this.prisma.submission.count({
          where: {
            userId: updatedSubmission.userId,
            problemId: problemId,
          },
        });

        await this.adaptiveService
          .updateAfterSubmission({
            studentId: updatedSubmission.userId,
            problemId: problemId,
            isCorrect: result.status === SubmissionStatus.ACCEPTED,
            attemptNumber: attemptCount,
            timeSpent: result.runtime ? Math.round(result.runtime / 1000) : 60,
          })
          .catch((error) => {
            this.logger.error(`Failed to update adaptive layers: ${error.message}`);
          });
      }
    } catch (error: any) {
      // Handle execution errors
      await this.prisma.submission.update({
        where: { id: submissionId },
        data: {
          status: SubmissionStatus.RUNTIME_ERROR,
          output: error.message || 'Unknown error occurred',
        },
      });
    }
  }

  async findByProblem(problemId: string, userId: string) {
    return this.prisma.submission.findMany({
      where: { problemId, userId },
      orderBy: { createdAt: 'desc' },
    });
  }

  async findById(id: string) {
    const submission = await this.prisma.submission.findUnique({ where: { id } });
    if (!submission) {
      throw new NotFoundException('Submission not found');
    }
    return submission;
  }

  async findByUser(userId: string) {
    return this.prisma.submission.findMany({
      where: { userId },
      include: { problem: { select: { id: true, title: true, difficulty: true } } },
      orderBy: { createdAt: 'desc' },
    });
  }

  private async updateUserSkills(userId: string): Promise<void> {
    try {
      const response = await fetch(`${this.aiServiceUrl}/profile/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Service-Key': this.aiServiceKey,
        },
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`AI service error: ${response.status} - ${text}`);
      }

      const data = await response.json();
      console.log(`✅ Updated skill profile for user ${userId}: ${data.skills.length} skills`);
    } catch (error: any) {
      console.error(`❌ Failed to update skills for user ${userId}:`, error.message);
      throw error;
    }
  }
}
