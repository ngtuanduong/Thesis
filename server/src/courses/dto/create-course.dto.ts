import { IsString, IsOptional } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateCourseDto {
  @ApiProperty({ example: 'Introduction to Python Programming' })
  @IsString()
  title: string;

  @ApiPropertyOptional({ example: 'A beginner-friendly course covering Python fundamentals.' })
  @IsString()
  @IsOptional()
  description?: string;
}
