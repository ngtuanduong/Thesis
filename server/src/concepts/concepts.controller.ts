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
import { ConceptsService } from './concepts.service';
import { CreateConceptDto } from './dto/create-concept.dto';
import { UpdateConceptDto } from './dto/update-concept.dto';
import { CreateEdgeDto } from './dto/create-edge.dto';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';
import { Role } from '@prisma/client';

@Controller('concepts')
@UseGuards(AuthGuard('jwt'))
export class ConceptsController {
  constructor(private conceptsService: ConceptsService) {}

  @Get()
  findAll() {
    return this.conceptsService.findAll();
  }

  @Get('graph')
  getKnowledgeGraph() {
    return this.conceptsService.getKnowledgeGraph();
  }

  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.conceptsService.findById(id);
  }

  @Post()
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  create(@Body() dto: CreateConceptDto) {
    return this.conceptsService.create(dto);
  }

  @Put(':id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  update(@Param('id', ParseIntPipe) id: number, @Body() dto: UpdateConceptDto) {
    return this.conceptsService.update(id, dto);
  }

  @Post('edges')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  createEdge(@Body() dto: CreateEdgeDto) {
    return this.conceptsService.createEdge(dto);
  }

  @Delete('edges/:id')
  @UseGuards(RolesGuard)
  @Roles(Role.INSTRUCTOR, Role.ADMIN)
  deleteEdge(@Param('id', ParseIntPipe) id: number) {
    return this.conceptsService.deleteEdge(id);
  }
}
