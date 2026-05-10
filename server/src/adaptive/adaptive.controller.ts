import { Body, Controller, Get, Param, Post, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiQuery, ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsString, IsOptional, IsNumber } from 'class-validator';
import { AdaptiveService } from './adaptive.service';
import { CurrentUser } from '../common/decorators/current-user.decorator';

class GenerateHintDto {
  @ApiProperty({ description: 'Student user ID' })
  @IsString()
  studentId: string;

  @ApiProperty({ description: 'Problem ID' })
  @IsString()
  problemId: string;

  @ApiProperty({ description: 'Current student code' })
  @IsString()
  code: string;

  @ApiPropertyOptional({ description: 'Error message from last execution' })
  @IsString()
  @IsOptional()
  errorMessage?: string;

  @ApiPropertyOptional({ description: 'Hint level (1=gentle, 2=specific, 3=detailed)', default: 1 })
  @IsNumber()
  @IsOptional()
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

  @Get('review-cards/:userId')
  @ApiOperation({ summary: 'Get all FSRS review cards with full statistics' })
  getReviewCards(@Param('userId') userId: string) {
    return this.adaptiveService.getReviewCards(userId);
  }

  @Get('practice/:userId/:conceptId')
  @ApiOperation({ summary: 'Get best practice problem for a concept via MAB' })
  getPracticeForConcept(
    @Param('userId') userId: string,
    @Param('conceptId') conceptId: string,
  ) {
    return this.adaptiveService.getPracticeForConcept(userId, parseInt(conceptId));
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
