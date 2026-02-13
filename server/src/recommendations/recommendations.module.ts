import { Module } from '@nestjs/common';
import { RecommendationsService } from './recommendations.service';
import { RecommendationsController } from './recommendations.controller';
import { SkillsModule } from '../skills/skills.module';
import { ProblemsModule } from '../problems/problems.module';
import { AiModule } from '../ai/ai.module';

@Module({
  imports: [SkillsModule, ProblemsModule, AiModule],
  controllers: [RecommendationsController],
  providers: [RecommendationsService],
})
export class RecommendationsModule {}
