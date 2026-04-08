import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  ParseIntPipe,
  UseGuards,
} from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { ConceptsService } from './concepts.service';
import { CreateConceptDto } from './dto/create-concept.dto';
import { UpdateConceptDto } from './dto/update-concept.dto';
import { CreateEdgeDto } from './dto/create-edge.dto';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@ApiTags('Concepts')
@ApiBearerAuth('JWT')
@Controller('concepts')
@UseGuards(AuthGuard('jwt'))
export class ConceptsController {
  constructor(private conceptsService: ConceptsService) {}

  @Get()
  @ApiOperation({ summary: 'List all concepts with associated problems' })
  findAll() {
    return this.conceptsService.findAll();
  }

  @Get('graph')
  @ApiOperation({ summary: 'Get full knowledge graph (nodes + edges)' })
  getKnowledgeGraph() {
    return this.conceptsService.getKnowledgeGraph();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get concept by ID with prerequisites and dependents' })
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.conceptsService.findById(id);
  }

  @Post()
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Create a new concept (Instructor/Admin)' })
  create(@Body() dto: CreateConceptDto) {
    return this.conceptsService.create(dto);
  }

  @Put(':id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Update a concept (Instructor/Admin)' })
  update(@Param('id', ParseIntPipe) id: number, @Body() dto: UpdateConceptDto) {
    return this.conceptsService.update(id, dto);
  }

  @Post('edges')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Create a prerequisite edge between concepts' })
  createEdge(@Body() dto: CreateEdgeDto) {
    return this.conceptsService.createEdge(dto);
  }

  @Delete('edges/:id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  @ApiOperation({ summary: 'Delete a prerequisite edge' })
  deleteEdge(@Param('id', ParseIntPipe) id: number) {
    return this.conceptsService.deleteEdge(id);
  }
}
