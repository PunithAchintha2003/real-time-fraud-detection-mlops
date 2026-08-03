import { Controller, Get, UseGuards } from '@nestjs/common';

import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { CurrentUser } from '../auth/decorators/current-user.decorator';
import { CurrentUserType } from '../auth/types/current-user.type';

@Controller('users')
export class UsersController {
  @Get('me')
  @UseGuards(JwtAuthGuard)
  getCurrentUser(@CurrentUser() user: CurrentUserType) {
    return {
      user,
    };
  }
}
