import { IsString } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class CreateSubmissionDto {
  @ApiProperty({ description: 'ID of the problem to solve' })
  @IsString()
  problemId: string;

  @ApiProperty({ example: 'print("Hello, World!")', description: 'Source code to execute' })
  @IsString()
  code: string;

  @ApiProperty({ example: 'python', description: 'Programming language' })
  @IsString()
  language: string;
}
