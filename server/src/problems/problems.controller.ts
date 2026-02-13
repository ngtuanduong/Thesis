import { Controller, Get, Post, Body, Param, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ProblemsService } from './problems.service';
import { CreateProblemDto } from './dto/create-problem.dto';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@Controller('problems')
@UseGuards(AuthGuard('jwt'))
export class ProblemsController {
  constructor(private problemsService: ProblemsService) {}

  @Post()
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  create(@Body() dto: CreateProblemDto) {
    return this.problemsService.create(dto);
  }

  @Get()
  findAll(@Query('courseId') courseId?: string) {
    return this.problemsService.findAll(courseId);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.problemsService.findById(id);
  }
}
