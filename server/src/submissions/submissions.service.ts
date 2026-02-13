import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateSubmissionDto } from './dto/create-submission.dto';

@Injectable()
export class SubmissionsService {
  constructor(private prisma: PrismaService) {}

  async create(dto: CreateSubmissionDto, userId: string) {
    return this.prisma.submission.create({
      data: { ...dto, userId },
    });
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
}
