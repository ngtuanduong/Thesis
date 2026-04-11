import { Test, TestingModule } from '@nestjs/testing';
import { NotFoundException } from '@nestjs/common';
import { ConceptsService } from './concepts.service';
import { PrismaService } from '../prisma/prisma.service';

describe('ConceptsService', () => {
  let service: ConceptsService;
  let prisma: Record<string, any>;

  const mockConcept = {
    id: 1,
    name: 'arrays',
    displayName: 'Arrays',
    topicGroup: 'data-structures',
    difficultyTier: 1,
    problemConcepts: [],
  };

  const mockEdge = {
    id: 1,
    fromConceptId: 1,
    toConceptId: 2,
    relationType: 'PREREQUISITE',
    weight: 1.0,
  };

  beforeEach(async () => {
    prisma = {
      concept: {
        findMany: jest.fn(),
        findUnique: jest.fn(),
        create: jest.fn(),
        update: jest.fn(),
      },
      knowledgeGraphEdge: {
        findMany: jest.fn(),
        create: jest.fn(),
        delete: jest.fn(),
      },
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ConceptsService,
        { provide: PrismaService, useValue: prisma },
      ],
    }).compile();

    service = module.get<ConceptsService>(ConceptsService);
  });

  describe('findAll', () => {
    it('should return concepts with problems ordered by tier and name', async () => {
      prisma.concept.findMany.mockResolvedValue([mockConcept]);

      const result = await service.findAll();

      expect(prisma.concept.findMany).toHaveBeenCalledWith({
        orderBy: [{ difficultyTier: 'asc' }, { name: 'asc' }],
        include: {
          problemConcepts: {
            include: {
              problem: { select: { id: true, title: true, difficulty: true } },
            },
          },
        },
      });
      expect(result).toEqual([mockConcept]);
    });
  });

  describe('findById', () => {
    it('should return a concept with relations when found', async () => {
      const conceptWithRelations = {
        ...mockConcept,
        prerequisiteFor: [],
        hasPrerequisites: [],
      };
      prisma.concept.findUnique.mockResolvedValue(conceptWithRelations);

      const result = await service.findById(1);

      expect(prisma.concept.findUnique).toHaveBeenCalledWith({
        where: { id: 1 },
        include: {
          problemConcepts: {
            include: {
              problem: { select: { id: true, title: true, difficulty: true } },
            },
          },
          prerequisiteFor: {
            include: {
              toConcept: { select: { id: true, name: true, displayName: true } },
            },
          },
          hasPrerequisites: {
            include: {
              fromConcept: {
                select: { id: true, name: true, displayName: true },
              },
            },
          },
        },
      });
      expect(result).toEqual(conceptWithRelations);
    });

    it('should throw NotFoundException when concept not found', async () => {
      prisma.concept.findUnique.mockResolvedValue(null);

      await expect(service.findById(999)).rejects.toThrow(NotFoundException);
    });
  });

  describe('create', () => {
    it('should create a concept', async () => {
      const dto = {
        name: 'arrays',
        displayName: 'Arrays',
        topicGroup: 'data-structures',
        difficultyTier: 1,
      };
      prisma.concept.create.mockResolvedValue({ id: 1, ...dto });

      const result = await service.create(dto);

      expect(prisma.concept.create).toHaveBeenCalledWith({ data: dto });
      expect(result).toEqual({ id: 1, ...dto });
    });
  });

  describe('update', () => {
    it('should update a concept', async () => {
      const conceptWithRelations = {
        ...mockConcept,
        prerequisiteFor: [],
        hasPrerequisites: [],
      };
      prisma.concept.findUnique.mockResolvedValue(conceptWithRelations);
      const updated = { ...mockConcept, displayName: 'Updated Arrays' };
      prisma.concept.update.mockResolvedValue(updated);

      const result = await service.update(1, { displayName: 'Updated Arrays' });

      expect(prisma.concept.update).toHaveBeenCalledWith({
        where: { id: 1 },
        data: { displayName: 'Updated Arrays' },
      });
      expect(result).toEqual(updated);
    });
  });

  describe('getKnowledgeGraph', () => {
    it('should return nodes and edges for the knowledge graph', async () => {
      const nodes = [
        {
          id: 1,
          name: 'arrays',
          displayName: 'Arrays',
          topicGroup: 'data-structures',
          difficultyTier: 1,
        },
        {
          id: 2,
          name: 'sorting',
          displayName: 'Sorting',
          topicGroup: 'algorithms',
          difficultyTier: 2,
        },
      ];
      prisma.concept.findMany.mockResolvedValue(nodes);
      prisma.knowledgeGraphEdge.findMany.mockResolvedValue([mockEdge]);

      const result = await service.getKnowledgeGraph();

      expect(prisma.concept.findMany).toHaveBeenCalledWith({
        orderBy: { difficultyTier: 'asc' },
        select: {
          id: true,
          name: true,
          displayName: true,
          topicGroup: true,
          difficultyTier: true,
        },
      });
      expect(prisma.knowledgeGraphEdge.findMany).toHaveBeenCalledWith({
        select: {
          id: true,
          fromConceptId: true,
          toConceptId: true,
          relationType: true,
          weight: true,
        },
      });
      expect(result).toEqual({ nodes, edges: [mockEdge] });
    });
  });

  describe('createEdge', () => {
    it('should create a prerequisite edge with defaults', async () => {
      const dto = { fromConceptId: 1, toConceptId: 2 };
      prisma.knowledgeGraphEdge.create.mockResolvedValue(mockEdge);

      const result = await service.createEdge(dto);

      expect(prisma.knowledgeGraphEdge.create).toHaveBeenCalledWith({
        data: {
          fromConceptId: 1,
          toConceptId: 2,
          relationType: 'PREREQUISITE',
          weight: 1.0,
        },
      });
      expect(result).toEqual(mockEdge);
    });

    it('should create an edge with custom relationType and weight', async () => {
      const dto = {
        fromConceptId: 1,
        toConceptId: 2,
        relationType: 'RELATED',
        weight: 0.5,
      };
      const customEdge = { ...mockEdge, relationType: 'RELATED', weight: 0.5 };
      prisma.knowledgeGraphEdge.create.mockResolvedValue(customEdge);

      const result = await service.createEdge(dto);

      expect(prisma.knowledgeGraphEdge.create).toHaveBeenCalledWith({
        data: {
          fromConceptId: 1,
          toConceptId: 2,
          relationType: 'RELATED',
          weight: 0.5,
        },
      });
      expect(result).toEqual(customEdge);
    });
  });

  describe('deleteEdge', () => {
    it('should delete an edge by id', async () => {
      prisma.knowledgeGraphEdge.delete.mockResolvedValue(mockEdge);

      const result = await service.deleteEdge(1);

      expect(prisma.knowledgeGraphEdge.delete).toHaveBeenCalledWith({
        where: { id: 1 },
      });
      expect(result).toEqual(mockEdge);
    });
  });
});
