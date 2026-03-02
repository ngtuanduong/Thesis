import { IsInt, IsOptional, IsString, IsNumber } from 'class-validator';

export class CreateEdgeDto {
  @IsInt()
  fromConceptId: number;

  @IsInt()
  toConceptId: number;

  @IsOptional()
  @IsString()
  relationType?: string;

  @IsOptional()
  @IsNumber()
  weight?: number;
}
