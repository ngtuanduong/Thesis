import { IsString, MaxLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class SendMessageDto {
  @IsString()
  @MaxLength(1000)
  @ApiProperty({
    description: 'Chat message to send to AdaptBot',
    maxLength: 1000,
    example: 'How do I submit code on this platform?',
  })
  message: string;
}
