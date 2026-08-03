import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { JwtModule, JwtModuleOptions, JwtSignOptions } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';

import { PrismaModule } from '../database/prisma/prisma.module';

import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtStrategy } from './strategies/jwt.strategy';

@Module({
  imports: [
    PrismaModule,
    ConfigModule,

    PassportModule.register({
      defaultStrategy: 'jwt',
      session: false,
    }),

    JwtModule.registerAsync({
      global: true,
      imports: [ConfigModule],
      inject: [ConfigService],

      useFactory: (configService: ConfigService): JwtModuleOptions => {
        const jwtSecret = configService.get<string>('JWT_SECRET');

        const accessTokenExpiresIn =
          configService.get<JwtSignOptions['expiresIn']>(
            'JWT_ACCESS_EXPIRES',
          ) ?? '15m';

        if (!jwtSecret) {
          throw new Error('JWT_SECRET environment variable is not defined');
        }

        return {
          secret: jwtSecret,

          signOptions: {
            expiresIn: accessTokenExpiresIn,
          },
        };
      },
    }),
  ],

  controllers: [AuthController],

  providers: [AuthService, JwtStrategy],

  exports: [AuthService, JwtModule, PassportModule],
})
export class AuthModule {}
