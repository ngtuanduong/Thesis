import { Test, TestingModule } from '@nestjs/testing';
import { NotFoundException } from '@nestjs/common';
import { CoursesService } from './courses.service';
import { PrismaService } from '../prisma/prisma.service';

describe('CoursesService', () => {
  let service: CoursesService;
  let prisma: Record<string, any>;

  const mockCourse = {
    id: 'course-1',
    title: 'Python Basics',
    description: 'Learn Python from scratch',
    instructorId: 'instructor-1',
    instructor: { id: 'instructor-1', name: 'Dr. Smith' },
    problems: [],
    createdAt: new Date(),
  };

  beforeEach(async () => {
    prisma = {
      course: {
        create: jest.fn(),
        findMany: jest.fn(),
        findUnique: jest.fn(),
      },
      enrollment: {
        create: jest.fn(),
      },
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CoursesService,
        { provide: PrismaService, useValue: prisma },
      ],
    }).compile();

    service = module.get<CoursesService>(CoursesService);
  });

  describe('create', () => {
    it('should create a course with instructor ID', async () => {
      prisma.course.create.mockResolvedValue(mockCourse);

      const dto = { title: 'Python Basics', description: 'Learn Python from scratch' };
      const result = await service.create(dto, 'instructor-1');

      expect(prisma.course.create).toHaveBeenCalledWith({
        data: { ...dto, instructorId: 'instructor-1' },
      });
      expect(result).toEqual(mockCourse);
    });
  });

  describe('findAll', () => {
    it('should return courses with instructor info', async () => {
      prisma.course.findMany.mockResolvedValue([mockCourse]);

      const result = await service.findAll();

      expect(prisma.course.findMany).toHaveBeenCalledWith({
        include: { instructor: { select: { id: true, name: true } } },
      });
      expect(result).toEqual([mockCourse]);
    });
  });

  describe('findById', () => {
    it('should return course with problems when found', async () => {
      prisma.course.findUnique.mockResolvedValue(mockCourse);

      const result = await service.findById('course-1');

      expect(prisma.course.findUnique).toHaveBeenCalledWith({
        where: { id: 'course-1' },
        include: {
          instructor: { select: { id: true, name: true } },
          problems: true,
        },
      });
      expect(result).toEqual(mockCourse);
    });

    it('should throw NotFoundException when course not found', async () => {
      prisma.course.findUnique.mockResolvedValue(null);

      await expect(service.findById('nonexistent')).rejects.toThrow(
        NotFoundException,
      );
    });
  });

  describe('enroll', () => {
    it('should create enrollment record', async () => {
      const mockEnrollment = {
        id: 'enroll-1',
        courseId: 'course-1',
        userId: 'user-1',
        createdAt: new Date(),
      };
      prisma.enrollment.create.mockResolvedValue(mockEnrollment);

      const result = await service.enroll('course-1', 'user-1');

      expect(prisma.enrollment.create).toHaveBeenCalledWith({
        data: { courseId: 'course-1', userId: 'user-1' },
      });
      expect(result).toEqual(mockEnrollment);
    });

    it('should throw on duplicate enrollment (Prisma unique constraint)', async () => {
      const prismaError = new Error('Unique constraint failed');
      (prismaError as any).code = 'P2002';
      prisma.enrollment.create.mockRejectedValue(prismaError);

      await expect(service.enroll('course-1', 'user-1')).rejects.toThrow();
    });
  });
});
