import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Query,
  UseGuards,
} from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import {
  ApiTags,
  ApiOperation,
  ApiBearerAuth,
  ApiQuery,
} from '@nestjs/swagger';
import { AdminService } from './admin.service';
import { AssignGroupDto } from './dto/assign-group.dto';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@ApiTags('Admin')
@ApiBearerAuth('JWT')
@Controller('admin')
@UseGuards(AuthGuard('jwt'), RolesGuard)
@Roles(Role.ADMIN)
export class AdminController {
  constructor(private adminService: AdminService) {}

  @Get('stats')
  @ApiOperation({ summary: 'Get platform statistics (Admin only)' })
  getStats() {
    return this.adminService.getStats();
  }

  @Get('users')
  @ApiOperation({ summary: 'List all users with submission counts (Admin only)' })
  getUsers() {
    return this.adminService.getUsers();
  }

  @Post('users/:id/assign-group')
  @ApiOperation({ summary: 'Assign a user to an experiment group (Admin only)' })
  assignGroup(@Param('id') userId: string, @Body() dto: AssignGroupDto) {
    return this.adminService.assignGroup(userId, dto.groupName);
  }

  @Get('experiment')
  @ApiOperation({ summary: 'Get experiment/A-B test statistics (Admin only)' })
  getExperimentStats() {
    return this.adminService.getExperimentStats();
  }

  @Get('export/events')
  @ApiOperation({ summary: 'Export event logs, optionally filtered by event type (Admin only)' })
  @ApiQuery({ name: 'event', required: false, type: String, description: 'Filter by event type' })
  exportEvents(@Query('event') event?: string) {
    return this.adminService.exportEvents(event);
  }
}
