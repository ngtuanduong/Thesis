import { Module } from '@nestjs/common';
import { AdaptiveService } from './adaptive.service';
import { AdaptiveController } from './adaptive.controller';
import { AiModule } from '../ai/ai.module';

@Module({
  imports: [AiModule],
  controllers: [AdaptiveController],
  providers: [AdaptiveService],
  exports: [AdaptiveService],
})
export class AdaptiveModule {}
