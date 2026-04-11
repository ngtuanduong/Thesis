import { Controller, Get, Param, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { InstructorService } from './instructor.service';
import { FindProblemsManageQueryDto } from './dto/find-problems-manage-query.dto';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@ApiTags('Instructor')
@ApiBearerAuth('JWT')
@Controller('instructor')
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.INSTRUCTOR, Role.ADMIN)
export class InstructorController {
  constructor(private instructorService: InstructorService) {}

  @Get('dashboard/:courseId')
  @ApiOperation({ summary: 'Get course dashboard with enrollment, submission, and mastery stats (Instructor/Admin)' })
  getDashboard(@Param('courseId') courseId: string) {
    return this.instructorService.getDashboard(courseId);
  }

  @Get('students/:courseId')
  @ApiOperation({ summary: 'List enrolled students with performance metrics (Instructor/Admin)' })
  getStudents(@Param('courseId') courseId: string) {
    return this.instructorService.getStudents(courseId);
  }

  @Get('problems/manage')
  @ApiOperation({ summary: 'List problems with submission stats, concepts, and pagination (Instructor/Admin)' })
  getProblemsManage(@Query() query: FindProblemsManageQueryDto) {
    return this.instructorService.getProblemsManage({
      page: query.page ?? 1,
      pageSize: query.pageSize ?? 10,
      search: query.search || undefined,
      courseId: query.courseId || undefined,
    });
  }
}
