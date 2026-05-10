import { ForbiddenException, Injectable, Logger } from '@nestjs/common';
import { Role } from '@prisma/client';
import { PrismaService } from '../prisma/prisma.service';
import { AiService } from '../ai/ai.service';

const TOKEN_BUDGET: Record<Role, number> = {
  STUDENT: 5000,
  INSTRUCTOR: 15000,
  ADMIN: 50000,
};

@Injectable()
export class ChatbotService {
  private readonly logger = new Logger(ChatbotService.name);

  constructor(
    private prisma: PrismaService,
    private aiService: AiService,
  ) {}

  /** Send a message and get an AI response. Enforces daily token budget. */
  async sendMessage(userId: string, userRole: Role, message: string) {
    const budget = TOKEN_BUDGET[userRole];
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Check token budget
    const usage = await this.prisma.chatTokenUsage.findUnique({
      where: { userId_date: { userId, date: today } },
    });
    if (usage && usage.tokensUsed >= budget) {
      throw new ForbiddenException(
        `Daily token limit reached (${budget} tokens). Resets at midnight.`,
      );
    }

    // Fetch last 20 messages for LLM context
    const recentMessages = await this.prisma.chatMessage.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' },
      take: 20,
    });
    const conversationHistory = recentMessages.reverse().map((m) => ({
      role: m.role,
      content: m.content,
    }));

    // Save user message
    await this.prisma.chatMessage.create({
      data: { userId, role: 'user', content: message, tokens: 0 },
    });

    // Call AI service
    let responseContent: string;
    let tokensUsed = 0;

    try {
      const result = await this.aiService.chatbotRespond({
        message,
        conversationHistory,
        userRole,
      });

      if (result.error && !result.response) {
        responseContent =
          'I\'m temporarily unavailable. Please try again shortly.';
        this.logger.warn(`Chatbot AI error: ${result.error}`);
      } else {
        responseContent = result.response ?? 'No response generated.';
        tokensUsed = result.tokens_used ?? 0;
      }
    } catch (error) {
      this.logger.error(`Chatbot AI service call failed: ${error}`);
      responseContent =
        'I\'m temporarily unavailable. Please try again shortly.';
    }

    // Save assistant message
    const assistantMessage = await this.prisma.chatMessage.create({
      data: {
        userId,
        role: 'assistant',
        content: responseContent,
        tokens: tokensUsed,
      },
    });

    // Update daily token usage
    const updatedUsage = await this.prisma.chatTokenUsage.upsert({
      where: { userId_date: { userId, date: today } },
      update: { tokensUsed: { increment: tokensUsed } },
      create: { userId, date: today, tokensUsed },
    });

    return {
      id: assistantMessage.id,
      content: responseContent,
      tokens: tokensUsed,
      tokensRemaining: budget - updatedUsage.tokensUsed,
      createdAt: assistantMessage.createdAt,
    };
  }

  /** Get conversation history for a user. */
  async getHistory(userId: string, limit = 50) {
    return this.prisma.chatMessage.findMany({
      where: { userId },
      orderBy: { createdAt: 'asc' },
      take: Math.min(limit, 100),
    });
  }

  /** Clear all chat messages for a user. Does not reset token usage. */
  async clearHistory(userId: string) {
    await this.prisma.chatMessage.deleteMany({ where: { userId } });
    return { success: true };
  }

  /** Get today's token usage and limit for a user. */
  async getTokenUsage(userId: string, userRole: Role) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const usage = await this.prisma.chatTokenUsage.findUnique({
      where: { userId_date: { userId, date: today } },
    });

    return {
      tokensUsed: usage?.tokensUsed ?? 0,
      tokensLimit: TOKEN_BUDGET[userRole],
      date: today.toISOString().split('T')[0],
    };
  }
}
