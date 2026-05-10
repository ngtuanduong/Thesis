import { Module } from '@nestjs/common';
import { SubmissionsService } from './submissions.service';
import { SubmissionsController } from './submissions.controller';
import { CodeExecutionService } from './code-execution.service';
import { AdaptiveModule } from '../adaptive/adaptive.module';

@Module({
  imports: [AdaptiveModule],
  controllers: [SubmissionsController],
  providers: [SubmissionsService, CodeExecutionService],
  exports: [SubmissionsService],
})
export class SubmissionsModule {}
