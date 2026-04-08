import { Controller, Get, Post, Body, Param, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { SubmissionsService } from './submissions.service';
import { CreateSubmissionDto } from './dto/create-submission.dto';
import { CurrentUser } from '../common/decorators/current-user.decorator';

@ApiTags('Submissions')
@ApiBearerAuth('JWT')
@Controller('submissions')
@UseGuards(AuthGuard('jwt'))
export class SubmissionsController {
  constructor(private submissionsService: SubmissionsService) {}

  @Post()
  @ApiOperation({ summary: 'Submit code for a problem (executes in Docker sandbox)' })
  create(@Body() dto: CreateSubmissionDto, @CurrentUser() user: { id: string }) {
    return this.submissionsService.create(dto, user.id);
  }

  @Get('problem/:problemId')
  @ApiOperation({ summary: 'Get all submissions for a problem by the current user' })
  findByProblem(@Param('problemId') problemId: string, @CurrentUser() user: { id: string }) {
    return this.submissionsService.findByProblem(problemId, user.id);
  }

  @Get('my')
  @ApiOperation({ summary: 'Get all submissions by the current user' })
  findMine(@CurrentUser() user: { id: string }) {
    return this.submissionsService.findByUser(user.id);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get submission by ID' })
  findOne(@Param('id') id: string) {
    return this.submissionsService.findById(id);
  }
}
