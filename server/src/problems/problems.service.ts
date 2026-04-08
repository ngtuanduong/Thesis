import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';
import { CreateProblemDto } from './dto/create-problem.dto';

@Injectable()
export class ProblemsService {
  private readonly logger = new Logger(ProblemsService.name);

  constructor(
    private prisma: PrismaService,
    private aiService: AiService,
  ) {}

  async create(dto: CreateProblemDto) {
    const { testCases, ...problemData } = dto;
    const problem = await this.prisma.problem.create({
      data: {
        ...problemData,
        testCases: testCases ? { create: testCases } : undefined,
      },
      include: { testCases: true },
    });

    // Fire-and-forget: generate embedding for the new problem
    this.aiService.embedProblem(problem).catch((err) => {
      this.logger.warn(`Failed to embed problem ${problem.id}: ${err.message}`);
    });

    return problem;
  }

  async findAll(courseId?: string) {
    return this.prisma.problem.findMany({
      where: courseId ? { courseId } : undefined,
      include: { testCases: { where: { isHidden: false } } },
    });
  }

  async findById(id: string) {
    const problem = await this.prisma.problem.findUnique({
      where: { id },
      include: { testCases: true },
    });
    if (!problem) {
      throw new NotFoundException('Problem not found');
    }
    return problem;
  }

  async update(id: string, dto: Partial<CreateProblemDto>) {
    await this.findById(id); // throws NotFoundException if not found
    const { testCases, ...problemData } = dto;
    return this.prisma.problem.update({
      where: { id },
      data: {
        ...problemData,
        ...(testCases !== undefined && {
          testCases: {
            deleteMany: {},
            create: testCases,
          },
        }),
      },
      include: { testCases: true },
    });
  }

  async remove(id: string) {
    await this.findById(id);
    await this.prisma.problem.delete({ where: { id } });
    return { deleted: true };
  }
}
