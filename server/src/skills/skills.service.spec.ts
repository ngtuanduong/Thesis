import { Test, TestingModule } from '@nestjs/testing';
import { SkillsService } from './skills.service';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

describe('SkillsService', () => {
  let service: SkillsService;
  let prisma: Record<string, any>;
  let aiService: Record<string, any>;

  const mockSkill = {
    id: 'skill-1',
    userId: 'user-1',
    skillName: 'loops',
    score: 0.85,
    embedding: [0.1, 0.2, 0.3],
    updatedAt: new Date(),
  };

  beforeEach(async () => {
    prisma = {
      skillEmbedding: {
        findMany: jest.fn(),
        upsert: jest.fn(),
      },
    };

    aiService = {
      computeProfile: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        SkillsService,
        { provide: PrismaService, useValue: prisma },
        { provide: AiService, useValue: aiService },
      ],
    }).compile();

    service = module.get<SkillsService>(SkillsService);
  });

  describe('getByUser', () => {
    it('should return skills sorted by score desc', async () => {
      const skills = [
        { ...mockSkill, skillName: 'loops', score: 0.9 },
        { ...mockSkill, skillName: 'arrays', score: 0.7 },
      ];
      prisma.skillEmbedding.findMany.mockResolvedValue(skills);

      const result = await service.getByUser('user-1');

      expect(prisma.skillEmbedding.findMany).toHaveBeenCalledWith({
        where: { userId: 'user-1' },
        orderBy: { score: 'desc' },
      });
      expect(result).toEqual(skills);
    });

    it('should return empty array when user has no skills', async () => {
      prisma.skillEmbedding.findMany.mockResolvedValue([]);

      const result = await service.getByUser('user-no-skills');
      expect(result).toEqual([]);
    });
  });

  describe('upsert', () => {
    it('should create new skill embedding when not exists', async () => {
      prisma.skillEmbedding.upsert.mockResolvedValue(mockSkill);

      const result = await service.upsert('user-1', 'loops', 0.85, [0.1, 0.2, 0.3]);

      expect(prisma.skillEmbedding.upsert).toHaveBeenCalledWith({
        where: { userId_skillName: { userId: 'user-1', skillName: 'loops' } },
        update: { score: 0.85, embedding: [0.1, 0.2, 0.3] },
        create: { userId: 'user-1', skillName: 'loops', score: 0.85, embedding: [0.1, 0.2, 0.3] },
      });
      expect(result).toEqual(mockSkill);
    });
  });

  describe('computeProfile', () => {
    it('should delegate to AiService.computeProfile', async () => {
      const profileResult = { skills: [{ name: 'loops', score: 0.9 }] };
      aiService.computeProfile.mockResolvedValue(profileResult);

      const result = await service.computeProfile('user-1');

      expect(aiService.computeProfile).toHaveBeenCalledWith('user-1');
      expect(result).toEqual(profileResult);
    });

    it('should propagate AI service errors', async () => {
      aiService.computeProfile.mockRejectedValue(new Error('AI service down'));

      await expect(service.computeProfile('user-1')).rejects.toThrow(
        'AI service down',
      );
    });
  });
});
