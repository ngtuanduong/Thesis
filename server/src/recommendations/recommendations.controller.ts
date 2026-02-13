import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { RecommendationsService } from './recommendations.service';
import { CurrentUser } from '../common/decorators/current-user.decorator';

@Controller('recommendations')
@UseGuards(AuthGuard('jwt'))
export class RecommendationsController {
  constructor(private recommendationsService: RecommendationsService) {}

  @Get()
  getRecommendations(
    @CurrentUser() user: { id: string },
    @Query('limit') limit?: string,
  ) {
    return this.recommendationsService.getRecommendations(
      user.id,
      limit ? parseInt(limit, 10) : undefined,
    );
  }
}
