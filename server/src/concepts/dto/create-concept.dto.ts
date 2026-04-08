import { IsString, IsOptional, IsInt, Min, Max } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

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

  @ApiPropertyOptional({ example: 'Foundations', description: 'Topic grouping for organization' })
  @IsOptional()
  @IsString()
  topicGroup?: string;

  @ApiPropertyOptional({ example: 1, minimum: 1, maximum: 3, description: 'Difficulty tier (1-3)' })
  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(3)
  difficultyTier?: number;
}
