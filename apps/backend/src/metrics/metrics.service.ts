import { Injectable } from '@nestjs/common';
import {
  collectDefaultMetrics,
  Counter,
  Gauge,
  Histogram,
  Registry,
} from 'prom-client';

type HttpMetricLabels = 'method' | 'route' | 'status_code';

@Injectable()
export class MetricsService {
  private readonly registry = new Registry();

  private readonly httpRequestsTotal: Counter<HttpMetricLabels>;

  private readonly httpRequestDurationSeconds: Histogram<HttpMetricLabels>;

  private readonly appInfo: Gauge<'service' | 'version'>;

  constructor() {
    collectDefaultMetrics({
      register: this.registry,
      prefix: 'fraud_backend_',
    });

    this.httpRequestsTotal = new Counter({
      name: 'fraud_backend_http_requests_total',
      help: 'Total number of HTTP requests handled by the backend service.',
      labelNames: ['method', 'route', 'status_code'],
      registers: [this.registry],
    });

    this.httpRequestDurationSeconds = new Histogram({
      name: 'fraud_backend_http_request_duration_seconds',
      help: 'HTTP request duration in seconds for the backend service.',
      labelNames: ['method', 'route', 'status_code'],
      buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
      registers: [this.registry],
    });

    this.appInfo = new Gauge({
      name: 'fraud_backend_app_info',
      help: 'Backend application information.',
      labelNames: ['service', 'version'],
      registers: [this.registry],
    });

    this.appInfo.set(
      {
        service: 'fraud-detection-backend',
        version: process.env.npm_package_version ?? '0.0.1',
      },
      1,
    );
  }

  observeHttpRequest(
    method: string,
    route: string,
    statusCode: string,
    durationSeconds: number,
  ) {
    this.httpRequestsTotal.labels(method, route, statusCode).inc();
    this.httpRequestDurationSeconds
      .labels(method, route, statusCode)
      .observe(durationSeconds);
  }

  async getMetrics(): Promise<string> {
    return this.registry.metrics();
  }

  getContentType(): string {
    return this.registry.contentType;
  }
}
