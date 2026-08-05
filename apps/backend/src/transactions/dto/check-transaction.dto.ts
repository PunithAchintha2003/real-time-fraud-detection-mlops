import {
  IsBoolean,
  IsInt,
  IsNotEmpty,
  IsNumber,
  IsString,
  Matches,
  Min,
} from 'class-validator';

export class CheckTransactionDto {
  @IsNumber()
  @Min(0)
  amount: number;

  @IsString()
  @IsNotEmpty()
  merchant_type: string;

  @IsString()
  @IsNotEmpty()
  location: string;

  @IsString()
  @Matches(/^([01]\d|2[0-3]):[0-5]\d$/)
  transaction_time: string;

  @IsString()
  @IsNotEmpty()
  payment_method: string;

  @IsString()
  @IsNotEmpty()
  device_type: string;

  @IsBoolean()
  is_international: boolean;

  @IsInt()
  @Min(0)
  previous_failed_attempts: number;
}
