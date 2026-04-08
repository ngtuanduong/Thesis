import { Controller, Post, Body, Get, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';
import { RegisterDto } from './dto/register.dto';
import { CurrentUser } from '../common/decorators/current-user.decorator';
import { UsersService } from '../users/users.service';

@ApiTags('Auth')
@Controller('auth')
export class AuthController {
  constructor(
    private authService: AuthService,
    private usersService: UsersService,
  ) {}

  @Post('register')
  @ApiOperation({ summary: 'Register a new user account' })
  register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }

  @Post('login')
  @ApiOperation({ summary: 'Authenticate and receive JWT token' })
  login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }

  @Get('me')
  @UseGuards(AuthGuard('jwt'))
  @ApiBearerAuth('JWT')
  @ApiOperation({ summary: 'Get current authenticated user profile' })
  async getProfile(@CurrentUser() user: { id: string; role: string }) {
    const fullUser = await this.usersService.findById(user.id);
    return {
      id: fullUser.id,
      email: fullUser.email,
      name: fullUser.name,
      role: fullUser.role,
    };
  }
}
