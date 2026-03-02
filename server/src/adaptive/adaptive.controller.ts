import { Body, Controller, Get, Param, Post, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { AdaptiveService } from './adaptive.service';

@Controller('adaptive')
@UseGuards(AuthGuard('jwt'))
export class AdaptiveController {
  constructor(private adaptiveService: AdaptiveService) {}

  @Get('recommend/:userId')
  getRecommendations(
    @Param('userId') userId: string,
    @Query('limit') limit?: string,
  ) {
    return this.adaptiveService.getRecommendations(userId, limit ? parseInt(limit) : 5);
  }

  @Get('knowledge-state/:userId')
  getKnowledgeState(@Param('userId') userId: string) {
    return this.adaptiveService.getKnowledgeState(userId);
  }

  @Get('review-queue/:userId')
  getReviewQueue(@Param('userId') userId: string) {
    return this.adaptiveService.getReviewQueue(userId);
  }

  @Post('hints')
  generateHint(
    @Body()
    body: {
      studentId: string;
      problemId: string;
      code: string;
      errorMessage?: string;
      hintLevel?: number;
    },
  ) {
    return this.adaptiveService.generateHint(body);
  }
}
