import { Controller, Get, Param, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { UsersService } from './users.service';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@ApiTags('Users')
@ApiBearerAuth('JWT')
@Controller('users')
@UseGuards(AuthGuard('jwt'))
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  @UseGuards(RolesGuard)
  @Roles(Role.ADMIN, Role.INSTRUCTOR)
  @ApiOperation({ summary: 'List all users (Instructor/Admin only)' })
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get user by ID' })
  findOne(@Param('id') id: string) {
    return this.usersService.findById(id);
  }
}
