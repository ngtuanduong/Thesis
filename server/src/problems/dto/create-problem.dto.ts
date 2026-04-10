import {
  IsString,
  IsEnum,
  IsOptional,
  IsArray,
  ValidateNested,
  IsBoolean,
} from 'class-validator';
import { ApiProperty, ApiPropertyOptional, PartialType } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { Difficulty } from '@prisma/client';

class CreateTestCaseDto {
  @ApiProperty({ example: '5', description: 'Input for the test case' })
  @IsString()
  input: string;

  @ApiProperty({ example: '25', description: 'Expected output' })
  @IsString()
  expected: string;

  @ApiPropertyOptional({ default: false, description: 'Hidden from students' })
  @IsBoolean()
  @IsOptional()
  isHidden?: boolean;
}

export class CreateProblemDto {
  @ApiProperty({ example: 'Two Sum' })
  @IsString()
  title: string;

  @ApiProperty({ example: 'Given an array of integers, return indices of the two numbers that add up to a target.' })
  @IsString()
  description: string;

  @ApiPropertyOptional({ example: '- 2 ≤ nums.length ≤ 10⁴\n- -10⁹ ≤ nums[i] ≤ 10⁹', description: 'Input constraints' })
  @IsString()
  @IsOptional()
  constraints?: string;

  @ApiPropertyOptional({ enum: Difficulty, default: Difficulty.EASY })
  @IsEnum(Difficulty)
  @IsOptional()
  difficulty?: Difficulty;

  @ApiPropertyOptional({ description: 'Course ID to associate this problem with' })
  @IsString()
  @IsOptional()
  courseId?: string;

  @ApiPropertyOptional({ example: ['arrays', 'hash-map'], description: 'Problem tags' })
  @IsArray()
  @IsString({ each: true })
  @IsOptional()
  tags?: string[];

  @ApiPropertyOptional({
    example: 'def solution(nums, target):\n    # Write your code here\n    pass\n',
    description: 'Starter code template. Auto-generated from test cases if not provided.',
  })
  @IsString()
  @IsOptional()
  starterCode?: string;

  @ApiPropertyOptional({ type: [CreateTestCaseDto], description: 'Test cases for validation' })
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => CreateTestCaseDto)
  @IsOptional()
  testCases?: CreateTestCaseDto[];
}

export class UpdateProblemDto extends PartialType(CreateProblemDto) {}
