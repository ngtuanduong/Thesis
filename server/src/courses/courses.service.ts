import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateCourseDto } from './dto/create-course.dto';

@Injectable()
export class CoursesService {
  constructor(private prisma: PrismaService) {}

  async create(dto: CreateCourseDto, instructorId: string) {
    return this.prisma.course.create({
      data: { ...dto, instructorId },
    });
  }

  async findAll(userId?: string) {
    const courses = await this.prisma.course.findMany({
      include: {
        instructor: { select: { id: true, name: true } },
        _count: { select: { enrollments: true, problems: true } },
        enrollments: userId
          ? { where: { userId }, select: { id: true } }
          : false,
      },
    });

    return courses.map(({ enrollments, ...course }) => ({
      ...course,
      isEnrolled: Array.isArray(enrollments) && enrollments.length > 0,
    }));
  }

  async findById(id: string) {
    const course = await this.prisma.course.findUnique({
      where: { id },
      include: {
        instructor: { select: { id: true, name: true } },
        problems: true,
      },
    });
    if (!course) {
      throw new NotFoundException('Course not found');
    }
    return course;
  }

  async update(id: string, dto: CreateCourseDto) {
    return this.prisma.course.update({
      where: { id },
      data: { title: dto.title, description: dto.description },
    });
  }

  async remove(id: string) {
    return this.prisma.course.delete({ where: { id } });
  }

  async enroll(courseId: string, userId: string) {
    return this.prisma.enrollment.upsert({
      where: { userId_courseId: { userId, courseId } },
      create: { courseId, userId },
      update: {},
    });
  }
}
