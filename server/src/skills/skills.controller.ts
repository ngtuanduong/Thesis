import { Controller, Get, Post, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { SkillsService } from './skills.service';
import { CurrentUser } from '../common/decorators/current-user.decorator';

@Controller('skills')
@UseGuards(AuthGuard('jwt'))
export class SkillsController {
  constructor(private skillsService: SkillsService) {}

  @Get('me')
  getMySkills(@CurrentUser() user: { id: string }) {
    return this.skillsService.getByUser(user.id);
  }

  @Post('compute')
  computeProfile(@CurrentUser() user: { id: string }) {
    return this.skillsService.computeProfile(user.id);
  }
}
