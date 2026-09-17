import { Type } from 'class-transformer';
import { IsNumber, Min } from 'class-validator';

export class CheckCreditCardDto {
  @Type(() => Number)
  @IsNumber()
  @Min(0)
  Time: number;

  @Type(() => Number)
  @IsNumber()
  V1: number;

  @Type(() => Number)
  @IsNumber()
  V2: number;

  @Type(() => Number)
  @IsNumber()
  V3: number;

  @Type(() => Number)
  @IsNumber()
  V4: number;

  @Type(() => Number)
  @IsNumber()
  V5: number;

  @Type(() => Number)
  @IsNumber()
  V6: number;

  @Type(() => Number)
  @IsNumber()
  V7: number;

  @Type(() => Number)
  @IsNumber()
  V8: number;

  @Type(() => Number)
  @IsNumber()
  V9: number;

  @Type(() => Number)
  @IsNumber()
  V10: number;

  @Type(() => Number)
  @IsNumber()
  V11: number;

  @Type(() => Number)
  @IsNumber()
  V12: number;

  @Type(() => Number)
  @IsNumber()
  V13: number;

  @Type(() => Number)
  @IsNumber()
  V14: number;

  @Type(() => Number)
  @IsNumber()
  V15: number;

  @Type(() => Number)
  @IsNumber()
  V16: number;

  @Type(() => Number)
  @IsNumber()
  V17: number;

  @Type(() => Number)
  @IsNumber()
  V18: number;

  @Type(() => Number)
  @IsNumber()
  V19: number;

  @Type(() => Number)
  @IsNumber()
  V20: number;

  @Type(() => Number)
  @IsNumber()
  V21: number;

  @Type(() => Number)
  @IsNumber()
  V22: number;

  @Type(() => Number)
  @IsNumber()
  V23: number;

  @Type(() => Number)
  @IsNumber()
  V24: number;

  @Type(() => Number)
  @IsNumber()
  V25: number;

  @Type(() => Number)
  @IsNumber()
  V26: number;

  @Type(() => Number)
  @IsNumber()
  V27: number;

  @Type(() => Number)
  @IsNumber()
  V28: number;

  @Type(() => Number)
  @IsNumber()
  @Min(0)
  Amount: number;
}
