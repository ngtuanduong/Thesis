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

  async findAll() {
    return this.prisma.course.findMany({
      include: { instructor: { select: { id: true, name: true } } },
    });
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

  async enroll(courseId: string, userId: string) {
    return this.prisma.enrollment.create({
      data: { courseId, userId },
    });
  }
}
