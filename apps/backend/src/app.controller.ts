import { Controller, Get } from '@nestjs/common';

@Controller()
export class AppController {
  @Get()
  getRoot(): {
    name: string;
    status: string;
    version: string;
    timestamp: string;
  } {
    return {
      name: 'Real-Time Fraud Detection API',
      status: 'running',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
    };
  }
}
