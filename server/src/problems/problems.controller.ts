import { Controller, Get, Post, Put, Delete, Body, Param, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { ProblemsService } from './problems.service';
import { CreateProblemDto, UpdateProblemDto } from './dto/create-problem.dto';
import { FindProblemsQueryDto } from './dto/find-problems-query.dto';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@ApiTags('Problems')
@ApiBearerAuth('JWT')
@Controller('problems')
@UseGuards(AuthGuard('jwt'))
export class ProblemsController {
  constructor(private problemsService: ProblemsService) {}

  @Post()
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Create a new problem (Instructor/Admin)' })
  create(@Body() dto: CreateProblemDto) {
    return this.problemsService.create(dto);
  }

  @Get()
  @ApiOperation({ summary: 'List all problems, optionally filtered by course' })
  @ApiQuery({ name: 'courseId', required: false })
  findAll(@Query('courseId') courseId?: string) {
    return this.problemsService.findAll(courseId);
  }

  @Get('paginated')
  @ApiOperation({ summary: 'List problems with offset-based pagination' })
  findPaginated(@Query() query: FindProblemsQueryDto) {
    return this.problemsService.findPaginated({
      page: query.page ?? 1,
      pageSize: query.pageSize ?? 15,
      courseId: query.courseId || undefined,
      search: query.search || undefined,
      difficulty: query.difficulty ? query.difficulty.split(',') : undefined,
      tags: query.tags ? query.tags.split(',') : undefined,
    });
  }

  @Get('tags')
  @ApiOperation({ summary: 'Get all distinct problem tags' })
  getDistinctTags() {
    return this.problemsService.getDistinctTags();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get problem by ID with test cases' })
  findOne(@Param('id') id: string) {
    return this.problemsService.findById(id);
  }

  @Put(':id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Update a problem (Instructor/Admin)' })
  update(@Param('id') id: string, @Body() dto: UpdateProblemDto) {
    return this.problemsService.update(id, dto);
  }

  @Delete(':id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Delete a problem (Instructor/Admin)' })
  remove(@Param('id') id: string) {
    return this.problemsService.remove(id);
  }
}
