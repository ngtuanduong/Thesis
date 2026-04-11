import { Module } from '@nestjs/common';
import { ProblemsService } from './problems.service';
import { ProblemsController } from './problems.controller';
import { AiModule } from '../ai/ai.module';

@Module({
  imports: [AiModule],
  controllers: [ProblemsController],
  providers: [ProblemsService],
  exports: [ProblemsService],
})
export class ProblemsModule {}
