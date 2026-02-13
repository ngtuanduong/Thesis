import { Controller, Get, Post, Body, Param, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { SubmissionsService } from './submissions.service';
import { CreateSubmissionDto } from './dto/create-submission.dto';
import { CurrentUser } from '../common/decorators/current-user.decorator';

@Controller('submissions')
@UseGuards(AuthGuard('jwt'))
export class SubmissionsController {
  constructor(private submissionsService: SubmissionsService) {}

  @Post()
  create(@Body() dto: CreateSubmissionDto, @CurrentUser() user: { id: string }) {
    return this.submissionsService.create(dto, user.id);
  }

  @Get('problem/:problemId')
  findByProblem(@Param('problemId') problemId: string, @CurrentUser() user: { id: string }) {
    return this.submissionsService.findByProblem(problemId, user.id);
  }

  @Get('my')
  findMine(@CurrentUser() user: { id: string }) {
    return this.submissionsService.findByUser(user.id);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.submissionsService.findById(id);
  }
}
