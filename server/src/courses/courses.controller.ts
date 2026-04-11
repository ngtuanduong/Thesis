import { Controller, Get, Post, Put, Delete, Body, Param, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { CoursesService } from './courses.service';
import { CreateCourseDto } from './dto/create-course.dto';
import { CurrentUser } from '../common/decorators/current-user.decorator';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@ApiTags('Courses')
@ApiBearerAuth('JWT')
@Controller('courses')
@UseGuards(AuthGuard('jwt'))
export class CoursesController {
  constructor(private coursesService: CoursesService) {}

  @Post()
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Create a new course (Instructor/Admin)' })
  create(@Body() dto: CreateCourseDto, @CurrentUser() user: { id: string }) {
    return this.coursesService.create(dto, user.id);
  }

  @Get()
  @ApiOperation({ summary: 'List all courses with enrollment counts' })
  findAll(@CurrentUser() user: { id: string }) {
    return this.coursesService.findAll(user.id);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get course by ID with problems' })
  findOne(@Param('id') id: string) {
    return this.coursesService.findById(id);
  }

  @Put(':id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Update a course (Instructor/Admin)' })
  update(@Param('id') id: string, @Body() dto: CreateCourseDto) {
    return this.coursesService.update(id, dto);
  }

  @Delete(':id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Delete a course (Instructor/Admin)' })
  remove(@Param('id') id: string) {
    return this.coursesService.remove(id);
  }

  @Post(':id/enroll')
  @ApiOperation({ summary: 'Enroll current student in a course' })
  enroll(@Param('id') courseId: string, @CurrentUser() user: { id: string }) {
    return this.coursesService.enroll(courseId, user.id);
  }
}
