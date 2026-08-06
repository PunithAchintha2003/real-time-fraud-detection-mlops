import { Injectable, NestMiddleware } from '@nestjs/common';
import type { NextFunction, Request, Response } from 'express';
import { MetricsService } from './metrics.service';

@Injectable()
export class MetricsMiddleware implements NestMiddleware {
  constructor(private readonly metricsService: MetricsService) {}

  use(req: Request, res: Response, next: NextFunction) {
    const startTime = process.hrtime.bigint();

    res.on('finish', () => {
      const durationSeconds =
        Number(process.hrtime.bigint() - startTime) / 1_000_000_000;

      this.metricsService.observeHttpRequest(
        req.method,
        this.getRoutePath(req),
        res.statusCode.toString(),
        durationSeconds,
      );
    });

    next();
  }

  private getRoutePath(req: Request): string {
    const path = req.path || req.originalUrl || 'unknown';

    return path
      .replace(
        /[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}/gi,
        ':id',
      )
      .replace(/\/\d+(?=\/|$)/g, '/:id');
  }
}
