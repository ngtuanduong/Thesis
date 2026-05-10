import { Controller, Get, Post, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { SkillsService } from './skills.service';
import { CurrentUser } from '../common/decorators/current-user.decorator';

@ApiTags('Skills')
@ApiBearerAuth('JWT')
@Controller('skills')
@UseGuards(AuthGuard('jwt'))
export class SkillsController {
  constructor(private skillsService: SkillsService) {}

  @Get('me')
  @ApiOperation({ summary: 'Get current user skill embeddings' })
  getMySkills(@CurrentUser() user: { id: string }) {
    return this.skillsService.getByUser(user.id);
  }

  @Post('compute')
  @ApiOperation({ summary: 'Recompute skill profile from submission history' })
  computeProfile(@CurrentUser() user: { id: string }) {
    return this.skillsService.computeProfile(user.id);
  }
}
