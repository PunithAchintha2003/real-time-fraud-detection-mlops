import { Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';

import { ExtractJwt, Strategy } from 'passport-jwt';

import { PrismaService } from '../../database/prisma/prisma.service';
import { UserStatus } from '../../generated/prisma/client';

import { JwtPayload } from '../types/jwt-payload.type';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, 'jwt') {
  constructor(
    private readonly prisma: PrismaService,
    configService: ConfigService,
  ) {
    const jwtSecret = configService.get<string>('JWT_SECRET');

    if (!jwtSecret) {
      throw new Error('JWT_SECRET environment variable is not defined');
    }

    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: jwtSecret,
    });
  }

  async validate(payload: JwtPayload) {
    if (payload.tokenType !== 'access') {
      throw new UnauthorizedException('Invalid access token type');
    }

    const user = await this.prisma.user.findUnique({
      where: {
        id: payload.sub,
      },
      select: {
        id: true,
        email: true,
        firstName: true,
        lastName: true,
        role: true,
        status: true,
      },
    });

    if (!user) {
      throw new UnauthorizedException('User account was not found');
    }

    if (user.status !== UserStatus.ACTIVE) {
      throw new UnauthorizedException('User account is not active');
    }

    return user;
  }
}
