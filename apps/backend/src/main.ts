import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);

  app.enableCors();

  const port = Number(process.env.PORT ?? 3001);

  await app.listen(port);

  console.log(`Backend running on http://localhost:${port}`);
}

bootstrap().catch((error: unknown) => {
  console.error('Failed to start backend:', error);
  process.exit(1);
});
