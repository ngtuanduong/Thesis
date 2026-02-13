import { IsString } from 'class-validator';

export class CreateSubmissionDto {
  @IsString()
  problemId: string;

  @IsString()
  code: string;

  @IsString()
  language: string;
}
