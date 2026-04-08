import { IsString } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class AssignGroupDto {
  @ApiProperty({ example: 'experimental', description: 'Experiment group name' })
  @IsString()
  groupName: string;
}
