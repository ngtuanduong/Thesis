import { IsString, IsOptional, IsInt, IsIn, Min, Max } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export const VALID_TOPIC_GROUPS = [
  'basics',
  'control_flow',
  'functions',
  'data_structures',
  'oop',
  'algorithms',
  'advanced',
] as const;

export class CreateConceptDto {
  @ApiProperty({ example: 'variables', description: 'Unique concept identifier' })
  @IsString()
  name: string;

  @ApiProperty({ example: 'Variables & Data Types', description: 'Human-readable name' })
  @IsString()
  displayName: string;

  @ApiPropertyOptional({ example: 'Understanding variables, assignment, and basic data types.' })
  @IsOptional()
  @IsString()
  description?: string;

  @ApiPropertyOptional({
    example: 'basics',
    enum: VALID_TOPIC_GROUPS,
    description: 'Topic group: basics, control_flow, functions, data_structures, oop, algorithms, advanced',
  })
  @IsOptional()
  @IsIn(VALID_TOPIC_GROUPS, { message: `topicGroup must be one of: ${VALID_TOPIC_GROUPS.join(', ')}` })
  topicGroup?: string;

  @ApiPropertyOptional({ example: 1, minimum: 1, maximum: 5, description: 'Difficulty tier (1-5)' })
  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(5)
  difficultyTier?: number;
}
