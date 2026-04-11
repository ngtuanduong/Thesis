import { IsInt, IsOptional, IsString, IsNumber } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateEdgeDto {
  @ApiProperty({ example: 1, description: 'Source concept ID (prerequisite)' })
  @IsInt()
  fromConceptId: number;

  @ApiProperty({ example: 2, description: 'Target concept ID (dependent)' })
  @IsInt()
  toConceptId: number;

  @ApiPropertyOptional({ example: 'PREREQUISITE', default: 'PREREQUISITE' })
  @IsOptional()
  @IsString()
  relationType?: string;

  @ApiPropertyOptional({ example: 1.0, default: 1.0, description: 'Edge weight (0-1)' })
  @IsOptional()
  @IsNumber()
  weight?: number;
}
