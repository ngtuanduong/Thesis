import { Module } from '@nestjs/common';
import { SubmissionsService } from './submissions.service';
import { SubmissionsController } from './submissions.controller';
import { CodeExecutionService } from './code-execution.service';

@Module({
  controllers: [SubmissionsController],
  providers: [SubmissionsService, CodeExecutionService],
  exports: [SubmissionsService],
})
export class SubmissionsModule {}
