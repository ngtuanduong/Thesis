import { Body, Controller, Get, Param, Post, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiQuery, ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { AdaptiveService } from './adaptive.service';
import { CurrentUser } from '../common/decorators/current-user.decorator';

class GenerateHintDto {
  @ApiProperty({ description: 'Student user ID' })
  studentId: string;

  @ApiProperty({ description: 'Problem ID' })
  problemId: string;

  @ApiProperty({ description: 'Current student code' })
  code: string;

  @ApiPropertyOptional({ description: 'Error message from last execution' })
  errorMessage?: string;

  @ApiPropertyOptional({ description: 'Hint level (1=gentle, 2=specific, 3=detailed)', default: 1 })
  hintLevel?: number;
}

@ApiTags('Adaptive')
@ApiBearerAuth('JWT')
@Controller('adaptive')
@UseGuards(AuthGuard('jwt'))
export class AdaptiveController {
  constructor(private adaptiveService: AdaptiveService) {}

  @Get('recommend/:userId')
  @ApiOperation({ summary: 'Get adaptive problem recommendations for a student' })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  getRecommendations(
    @Param('userId') userId: string,
    @Query('limit') limit?: string,
  ) {
    return this.adaptiveService.getRecommendations(userId, limit ? parseInt(limit) : 5);
  }

  @Get('knowledge-state/:userId')
  @ApiOperation({ summary: 'Get BKT knowledge state for all concepts' })
  getKnowledgeState(@Param('userId') userId: string) {
    return this.adaptiveService.getKnowledgeState(userId);
  }

  @Get('review-queue/:userId')
  @ApiOperation({ summary: 'Get FSRS spaced repetition review queue' })
  getReviewQueue(@Param('userId') userId: string) {
    return this.adaptiveService.getReviewQueue(userId);
  }

  @Post('hints')
  @ApiOperation({ summary: 'Generate Socratic hint using LLM (3 hint levels)' })
  generateHint(@Body() body: GenerateHintDto) {
    return this.adaptiveService.generateHint(body);
  }

  @Post('log-event')
  @ApiOperation({ summary: 'Log a frontend user interaction event for evaluation' })
  logEvent(
    @Body() body: { event: string; data?: Record<string, unknown>; sessionId?: string },
    @CurrentUser() user: { id: string },
  ) {
    return this.adaptiveService.logEvent({ userId: user.id, ...body });
  }

  @Get('elo-history/:userId')
  @ApiOperation({ summary: 'Get Elo rating history for trajectory visualization' })
  getEloHistory(@Param('userId') userId: string) {
    return this.adaptiveService.getEloHistory(userId);
  }
}
