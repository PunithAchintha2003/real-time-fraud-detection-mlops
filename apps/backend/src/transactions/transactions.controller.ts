import {
  Body,
  Controller,
  Get,
  Param,
  Post,
  Req,
  UseGuards,
} from '@nestjs/common';
import { Request } from 'express';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { CheckCreditCardDto } from './dto/check-credit-card.dto';
import { CheckTransactionDto } from './dto/check-transaction.dto';
import { TransactionsService } from './transactions.service';

type AuthenticatedRequest = Request & {
  user: {
    sub: string;
    email: string;
    role: string;
  };
};

@UseGuards(JwtAuthGuard)
@Controller('transactions')
export class TransactionsController {
  constructor(private readonly transactionsService: TransactionsService) {}

  @Post('check')
  checkTransaction(
    @Req() request: AuthenticatedRequest,
    @Body() checkTransactionDto: CheckTransactionDto,
  ) {
    return this.transactionsService.checkTransaction(
      request.user.sub,
      checkTransactionDto,
    );
  }

  @Post('check-credit-card')
  checkCreditCard(
    @Body() checkCreditCardDto: CheckCreditCardDto,
  ) {
    return this.transactionsService.checkCreditCard(
      checkCreditCardDto,
    );
  }

  @Get()
  findAll(@Req() request: AuthenticatedRequest) {
    return this.transactionsService.findAll(request.user.sub);
  }

  @Get(':id')
  findOne(
    @Req() request: AuthenticatedRequest,
    @Param('id') transactionId: string,
  ) {
    return this.transactionsService.findOne(request.user.sub, transactionId);
  }
}
