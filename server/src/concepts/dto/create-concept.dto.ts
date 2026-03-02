import { IsString, IsOptional, IsInt, Min, Max } from 'class-validator';

export class CreateConceptDto {
  @IsString()
  name: string;

  @IsString()
  displayName: string;

  @IsOptional()
  @IsString()
  description?: string;

  @IsOptional()
  @IsString()
  topicGroup?: string;

  @IsOptional()
  @IsInt()
  @Min(1)
  @Max(3)
  difficultyTier?: number;
}
