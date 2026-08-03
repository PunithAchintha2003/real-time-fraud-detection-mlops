import {
  ConflictException,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService, JwtSignOptions } from '@nestjs/jwt';

import { createHash, randomUUID, timingSafeEqual } from 'node:crypto';

import * as bcrypt from 'bcrypt';

import { PrismaService } from '../database/prisma/prisma.service';

import { LoginDto } from './dto/login.dto';
import { RegisterDto } from './dto/register.dto';
import { JwtPayload } from './types/jwt-payload.type';

@Injectable()
export class AuthService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
  ) {}

  async register(dto: RegisterDto) {
    const email = dto.email.trim().toLowerCase();

    const existingUser = await this.prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (existingUser) {
      throw new ConflictException('Email already registered');
    }

    const passwordHash = await bcrypt.hash(dto.password, 12);

    const user = await this.prisma.user.create({
      data: {
        email,
        passwordHash,
        firstName: dto.firstName.trim(),
        lastName: dto.lastName.trim(),
      },
    });

    const tokens = await this.generateTokens(user.id, user.email, user.role);

    await this.updateRefreshToken(user.id, tokens.refreshToken);

    return {
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
        status: user.status,
      },
      ...tokens,
    };
  }

  async login(dto: LoginDto) {
    const email = dto.email.trim().toLowerCase();

    const user = await this.prisma.user.findUnique({
      where: {
        email,
      },
    });

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    if (user.status !== 'ACTIVE') {
      throw new UnauthorizedException('User account is not active');
    }

    const passwordMatch = await bcrypt.compare(dto.password, user.passwordHash);

    if (!passwordMatch) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const tokens = await this.generateTokens(user.id, user.email, user.role);

    await this.updateRefreshToken(user.id, tokens.refreshToken);

    return {
      user: {
        id: user.id,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        role: user.role,
        status: user.status,
      },
      ...tokens,
    };
  }

  async refresh(refreshToken: string) {
    const refreshSecret = this.getRequiredConfig('JWT_REFRESH_SECRET');

    let payload: JwtPayload;

    try {
      payload = await this.jwtService.verifyAsync<JwtPayload>(refreshToken, {
        secret: refreshSecret,
      });
    } catch {
      throw new UnauthorizedException('Refresh token expired or invalid');
    }

    if (payload.tokenType !== 'refresh') {
      throw new UnauthorizedException('Invalid refresh token type');
    }

    const user = await this.prisma.user.findUnique({
      where: {
        id: payload.sub,
      },
    });

    if (!user || !user.refreshToken) {
      throw new UnauthorizedException('Refresh token expired or invalid');
    }

    if (user.status !== 'ACTIVE') {
      throw new UnauthorizedException('User account is not active');
    }

    const tokenMatch = this.compareRefreshToken(
      refreshToken,
      user.refreshToken,
    );

    if (!tokenMatch) {
      throw new UnauthorizedException('Refresh token expired or invalid');
    }

    const tokens = await this.generateTokens(user.id, user.email, user.role);

    await this.updateRefreshToken(user.id, tokens.refreshToken);

    return tokens;
  }

  async logout(userId: string) {
    await this.prisma.user.update({
      where: {
        id: userId,
      },
      data: {
        refreshToken: null,
      },
    });

    return {
      message: 'Logged out successfully',
    };
  }

  private async generateTokens(userId: string, email: string, role: string) {
    const accessSecret = this.getRequiredConfig('JWT_SECRET');

    const refreshSecret = this.getRequiredConfig('JWT_REFRESH_SECRET');

    const accessTokenExpiresIn =
      this.configService.get<JwtSignOptions['expiresIn']>(
        'JWT_ACCESS_EXPIRES',
      ) ?? '15m';

    const refreshTokenExpiresIn =
      this.configService.get<JwtSignOptions['expiresIn']>(
        'JWT_REFRESH_EXPIRES',
      ) ?? '7d';

    const accessPayload: JwtPayload = {
      sub: userId,
      email,
      role,
      tokenType: 'access',
      jti: randomUUID(),
    };

    const refreshPayload: JwtPayload = {
      sub: userId,
      email,
      role,
      tokenType: 'refresh',
      jti: randomUUID(),
    };

    const [accessToken, refreshToken] = await Promise.all([
      this.jwtService.signAsync(accessPayload, {
        secret: accessSecret,
        expiresIn: accessTokenExpiresIn,
      }),

      this.jwtService.signAsync(refreshPayload, {
        secret: refreshSecret,
        expiresIn: refreshTokenExpiresIn,
      }),
    ]);

    return {
      accessToken,
      refreshToken,
    };
  }

  private async updateRefreshToken(
    userId: string,
    refreshToken: string,
  ): Promise<void> {
    const refreshTokenHash = this.hashRefreshToken(refreshToken);

    await this.prisma.user.update({
      where: {
        id: userId,
      },
      data: {
        refreshToken: refreshTokenHash,
      },
    });
  }

  private hashRefreshToken(refreshToken: string): string {
    return createHash('sha256').update(refreshToken, 'utf8').digest('hex');
  }

  private compareRefreshToken(
    refreshToken: string,
    storedHash: string,
  ): boolean {
    const incomingHash = this.hashRefreshToken(refreshToken);

    const incomingBuffer = Buffer.from(incomingHash, 'hex');

    const storedBuffer = Buffer.from(storedHash, 'hex');

    if (incomingBuffer.length !== storedBuffer.length) {
      return false;
    }

    return timingSafeEqual(incomingBuffer, storedBuffer);
  }

  private getRequiredConfig(key: string): string {
    const value = this.configService.get<string>(key);

    if (!value) {
      throw new Error(`${key} environment variable is not defined`);
    }

    return value;
  }
}
