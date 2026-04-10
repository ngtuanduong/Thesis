import { IsOptional, IsString } from 'class-validator';
import { PaginationQueryDto } from '../../common/pagination';

export class FindProblemsQueryDto extends PaginationQueryDto {
  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @IsString()
  courseId?: string;

  @IsOptional()
  @IsString()
  difficulty?: string; // comma-separated, split in controller

  @IsOptional()
  @IsString()
  tags?: string; // comma-separated, split in controller
}
