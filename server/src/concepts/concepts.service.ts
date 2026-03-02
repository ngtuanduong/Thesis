import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateConceptDto } from './dto/create-concept.dto';
import { UpdateConceptDto } from './dto/update-concept.dto';
import { CreateEdgeDto } from './dto/create-edge.dto';

@Injectable()
export class ConceptsService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.concept.findMany({
      orderBy: [{ difficultyTier: 'asc' }, { name: 'asc' }],
      include: {
        problemConcepts: {
          include: { problem: { select: { id: true, title: true, difficulty: true } } },
        },
      },
    });
  }

  async findById(id: number) {
    const concept = await this.prisma.concept.findUnique({
      where: { id },
      include: {
        problemConcepts: {
          include: { problem: { select: { id: true, title: true, difficulty: true } } },
        },
        prerequisiteFor: {
          include: { toConcept: { select: { id: true, name: true, displayName: true } } },
        },
        hasPrerequisites: {
          include: { fromConcept: { select: { id: true, name: true, displayName: true } } },
        },
      },
    });
    if (!concept) {
      throw new NotFoundException('Concept not found');
    }
    return concept;
  }

  async create(dto: CreateConceptDto) {
    return this.prisma.concept.create({ data: dto });
  }

  async update(id: number, dto: UpdateConceptDto) {
    await this.findById(id);
    return this.prisma.concept.update({ where: { id }, data: dto });
  }

  async getKnowledgeGraph() {
    const concepts = await this.prisma.concept.findMany({
      orderBy: { difficultyTier: 'asc' },
      select: {
        id: true,
        name: true,
        displayName: true,
        topicGroup: true,
        difficultyTier: true,
      },
    });

    const edges = await this.prisma.knowledgeGraphEdge.findMany({
      select: {
        id: true,
        fromConceptId: true,
        toConceptId: true,
        relationType: true,
        weight: true,
      },
    });

    return { nodes: concepts, edges };
  }

  async createEdge(dto: CreateEdgeDto) {
    return this.prisma.knowledgeGraphEdge.create({
      data: {
        fromConceptId: dto.fromConceptId,
        toConceptId: dto.toConceptId,
        relationType: dto.relationType ?? 'PREREQUISITE',
        weight: dto.weight ?? 1.0,
      },
    });
  }

  async deleteEdge(id: number) {
    return this.prisma.knowledgeGraphEdge.delete({ where: { id } });
  }
}
