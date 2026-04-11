import { IsEmail, IsString, MinLength, IsEnum, IsOptional } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Role } from '@prisma/client';

export class RegisterDto {
  @ApiProperty({ example: 'student@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'password123', minLength: 6 })
  @IsString()
  @MinLength(6)
  password: string;

  @ApiProperty({ example: 'Nguyen Van A', minLength: 2 })
  @IsString()
  @MinLength(2)
  name: string;

  @ApiPropertyOptional({ enum: Role, default: Role.STUDENT })
  @IsEnum(Role)
  @IsOptional()
  role?: Role;
}
