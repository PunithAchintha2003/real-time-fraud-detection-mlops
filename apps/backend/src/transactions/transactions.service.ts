import {
  BadGatewayException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../prisma/prisma.service';
import { CheckTransactionDto } from './dto/check-transaction.dto';

type BusinessPredictionResponse = {
  prediction: number;
  is_fraud: boolean;
  fraud_probability: number;
  threshold: number;
  result: string;
  risk_level: string;
  model_type: string;
  model_version: string;
  features_used: number;
  engineered_features: Record<string, number>;
};

@Injectable()
export class TransactionsService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly configService: ConfigService,
  ) {}

  async checkTransaction(userId: string, dto: CheckTransactionDto) {
    const mlServiceUrl =
      this.configService.get<string>('ML_SERVICE_URL') ??
      'http://localhost:8000';

    let response: Response;

    try {
      response = await fetch(`${mlServiceUrl}/predict-business`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dto),
      });
    } catch {
      throw new BadGatewayException('Cannot connect to ML prediction service');
    }

    if (!response.ok) {
      throw new BadGatewayException('ML prediction service request failed');
    }

    const prediction = (await response.json()) as BusinessPredictionResponse;

    const transaction = await this.prisma.transaction.create({
      data: {
        userId,
        amount: dto.amount,
        merchantType: dto.merchant_type,
        location: dto.location,
        transactionTime: dto.transaction_time,
        paymentMethod: dto.payment_method,
        deviceType: dto.device_type,
        isInternational: dto.is_international,
        previousFailedAttempts: dto.previous_failed_attempts,
        prediction: {
          create: {
            prediction: prediction.prediction,
            isFraud: prediction.is_fraud,
            fraudProbability: prediction.fraud_probability,
            threshold: prediction.threshold,
            result: prediction.result,
            riskLevel: prediction.risk_level,
            modelType: prediction.model_type,
            modelVersion: prediction.model_version,
            featuresUsed: prediction.features_used,
            engineeredFeatures: prediction.engineered_features,
          },
        },
      },
      include: {
        prediction: true,
      },
    });

    return {
      transaction_id: transaction.id,
      prediction_id: transaction.prediction?.id,
      ...prediction,
    };
  }

  async findAll(userId: string) {
    return this.prisma.transaction.findMany({
      where: {
        userId,
      },
      include: {
        prediction: true,
      },
      orderBy: {
        createdAt: 'desc',
      },
    });
  }

  async findOne(userId: string, transactionId: string) {
    const transaction = await this.prisma.transaction.findFirst({
      where: {
        id: transactionId,
        userId,
      },
      include: {
        prediction: true,
      },
    });

    if (!transaction) {
      throw new NotFoundException('Transaction not found');
    }

    return transaction;
  }
}
