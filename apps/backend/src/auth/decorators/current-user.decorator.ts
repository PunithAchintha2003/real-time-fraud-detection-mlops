import { createParamDecorator, ExecutionContext } from '@nestjs/common';

import { CurrentUserType } from '../types/current-user.type';

export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext): CurrentUserType => {
    const request = ctx.switchToHttp().getRequest<{
      user: CurrentUserType;
    }>();

    return request.user;
  },
);
