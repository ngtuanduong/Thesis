import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
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

  async remove(id: number) {
    const concept = await this.findById(id);

    // Count related records that will be cascade-deleted
    const [problemCount, knowledgeStateCount, fsrsCardCount] = await Promise.all([
      this.prisma.problemConcept.count({ where: { conceptId: id } }),
      this.prisma.knowledgeState.count({ where: { conceptId: id } }),
      this.prisma.fsrsCard.count({ where: { conceptId: id } }),
    ]);

    if (knowledgeStateCount > 0) {
      throw new BadRequestException(
        `Cannot delete concept "${concept.displayName}": ${knowledgeStateCount} students have learning data for this concept. ` +
        `Deleting would permanently erase their progress.`,
      );
    }

    await this.prisma.concept.delete({ where: { id } });
    return {
      deleted: true,
      cascaded: { problems: problemCount, fsrsCards: fsrsCardCount },
    };
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
    // 1. Self-loop check
    if (dto.fromConceptId === dto.toConceptId) {
      throw new BadRequestException('A concept cannot be a prerequisite of itself');
    }

    // 2. Verify both concepts exist and get their tiers
    const [fromConcept, toConcept] = await Promise.all([
      this.prisma.concept.findUnique({ where: { id: dto.fromConceptId }, select: { id: true, displayName: true, difficultyTier: true } }),
      this.prisma.concept.findUnique({ where: { id: dto.toConceptId }, select: { id: true, displayName: true, difficultyTier: true } }),
    ]);
    if (!fromConcept) throw new NotFoundException(`Concept ${dto.fromConceptId} not found`);
    if (!toConcept) throw new NotFoundException(`Concept ${dto.toConceptId} not found`);

    // 3. Tier ordering: prerequisite tier must be <= dependent tier
    if (fromConcept.difficultyTier > toConcept.difficultyTier) {
      throw new BadRequestException(
        `Invalid tier ordering: "${fromConcept.displayName}" (tier ${fromConcept.difficultyTier}) ` +
        `cannot be a prerequisite of "${toConcept.displayName}" (tier ${toConcept.difficultyTier}). ` +
        `Prerequisites must be same or lower tier.`,
      );
    }

    // 4. Cycle detection via BFS: check if adding this edge creates a cycle
    //    Traverse from toConcept forward — if we reach fromConcept, it's a cycle
    const visited = new Set<number>();
    const queue = [dto.toConceptId];
    while (queue.length > 0) {
      const current = queue.shift()!;
      if (current === dto.fromConceptId) {
        throw new BadRequestException(
          `Adding this edge would create a cycle: there is already a path from ` +
          `"${toConcept.displayName}" to "${fromConcept.displayName}"`,
        );
      }
      if (visited.has(current)) continue;
      visited.add(current);
      const outEdges = await this.prisma.knowledgeGraphEdge.findMany({
        where: { fromConceptId: current },
        select: { toConceptId: true },
      });
      for (const edge of outEdges) {
        if (!visited.has(edge.toConceptId)) {
          queue.push(edge.toConceptId);
        }
      }
    }

    // 5. All validations passed — create the edge
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
