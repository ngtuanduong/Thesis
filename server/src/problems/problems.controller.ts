import { Controller, Get, Post, Put, Delete, Body, Param, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { ProblemsService } from './problems.service';
import { CreateProblemDto, UpdateProblemDto } from './dto/create-problem.dto';
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
