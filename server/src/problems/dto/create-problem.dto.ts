import {
  IsString,
  IsEnum,
  IsOptional,
  IsArray,
  ValidateNested,
  IsBoolean,
} from 'class-validator';
import { Type } from 'class-transformer';
import { Difficulty } from '@prisma/client';

class CreateTestCaseDto {
  @IsString()
  input: string;

  @IsString()
  expected: string;

  @IsBoolean()
  @IsOptional()
  isHidden?: boolean;
}

export class CreateProblemDto {
  @IsString()
  title: string;

  @IsString()
  description: string;

  @IsEnum(Difficulty)
  @IsOptional()
  difficulty?: Difficulty;

  @IsString()
  @IsOptional()
  courseId?: string;

  @IsArray()
  @IsString({ each: true })
  @IsOptional()
  tags?: string[];

  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => CreateTestCaseDto)
  @IsOptional()
  testCases?: CreateTestCaseDto[];
}
