import { NestFactory } from '@nestjs/core';
import { Logger, ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const logger = new Logger('Bootstrap');

  app.enableCors({
    origin: process.env.CLIENT_URL || 'http://localhost:5173',
    credentials: true,
  });

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );

  app.setGlobalPrefix('api');

  // Swagger/OpenAPI setup
  const swaggerConfig = new DocumentBuilder()
    .setTitle('AdaptLearn API')
    .setDescription(
      'Adaptive Learning Platform for University Programming Courses — ' +
        'RESTful API powering BKT, Elo, MAB, FSRS adaptive layers with Docker-sandboxed code execution.',
    )
    .setVersion('1.0')
    .addBearerAuth({ type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }, 'JWT')
    .addTag('Auth', 'Authentication & user registration')
    .addTag('Users', 'User profile management')
    .addTag('Courses', 'Course management & enrollment')
    .addTag('Problems', 'Programming problem CRUD')
    .addTag('Submissions', 'Code submission & execution')
    .addTag('Concepts', 'Knowledge graph concepts & edges')
    .addTag('Adaptive', 'Adaptive learning recommendations & state')
    .addTag('Skills', 'User skill embeddings')
    .addTag('Recommendations', 'Content-based recommendations')
    .build();
  const document = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup('api/docs', app, document);

  const port = process.env.PORT || 3000;
  await app.listen(port);
  logger.log(`Server running on http://localhost:${port}`);
  logger.log(`Swagger docs at http://localhost:${port}/api/docs`);
}

bootstrap();
