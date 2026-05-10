import {
  Body,
  Controller,
  Delete,
  Get,
  Post,
  Query,
  UseGuards,
} from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import {
  ApiBearerAuth,
  ApiOperation,
  ApiQuery,
  ApiTags,
} from '@nestjs/swagger';
import { Throttle } from '@nestjs/throttler';
import { Role } from '@prisma/client';
import { CurrentUser } from '../common/decorators/current-user.decorator';
import { ChatbotService } from './chatbot.service';
import { SendMessageDto } from './dto/send-message.dto';

@ApiTags('Chatbot')
@ApiBearerAuth('JWT')
@Controller('chatbot')
@UseGuards(AuthGuard('jwt'))
export class ChatbotController {
  constructor(private chatbotService: ChatbotService) {}

  @Post('send')
  @Throttle({ default: { limit: 10, ttl: 60000 } })
  @ApiOperation({ summary: 'Send a message to AdaptBot and receive a response' })
  send(
    @Body() dto: SendMessageDto,
    @CurrentUser() user: { id: string; role: Role },
  ) {
    return this.chatbotService.sendMessage(user.id, user.role, dto.message);
  }

  @Get('history')
  @ApiOperation({ summary: 'Get chat conversation history' })
  @ApiQuery({ name: 'limit', required: false, type: Number })
  getHistory(
    @CurrentUser() user: { id: string },
    @Query('limit') limit?: string,
  ) {
    return this.chatbotService.getHistory(user.id, limit ? parseInt(limit, 10) : 50);
  }

  @Delete('history')
  @ApiOperation({ summary: 'Clear chat conversation history' })
  clearHistory(@CurrentUser() user: { id: string }) {
    return this.chatbotService.clearHistory(user.id);
  }

  @Get('token-usage')
  @ApiOperation({ summary: 'Get daily token usage and limit' })
  getTokenUsage(@CurrentUser() user: { id: string; role: Role }) {
    return this.chatbotService.getTokenUsage(user.id, user.role);
  }
}
