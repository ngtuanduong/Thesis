import { Controller, Get, Query, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { RecommendationsService } from './recommendations.service';
import { CurrentUser } from '../common/decorators/current-user.decorator';

@ApiTags('Recommendations')
@ApiBearerAuth('JWT')
@Controller('recommendations')
@UseGuards(AuthGuard('jwt'))
export class RecommendationsController {
  constructor(private recommendationsService: RecommendationsService) {}

  @Get()
  @ApiOperation({ summary: 'Get content-based problem recommendations' })
  @ApiQuery({ name: 'limit', required: false, type: Number })
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
