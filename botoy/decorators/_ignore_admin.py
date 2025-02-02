import functools

from botoy.action import Action
from botoy.model import GroupMsg


@functools.lru_cache(520)
def __get_group_admins(qq, host, port, group):
    admins = Action(qq=qq, port=port, host=host).getGroupAdminList(group, True)
    return [admin["MemberUin"] for admin in admins]


def ignore_admin(func=None):
    """忽略来自群管理员(列表包括群主)的消息 GroupMsg
    管理员列表会进行``缓存``，调用520次后再次刷新, 所以可以放心使用"""
    if func is None:
        return ignore_admin

    def inner(ctx):
        assert isinstance(ctx, GroupMsg)
        admins = __get_group_admins(
            qq=ctx.CurrentQQ,
            host=getattr(ctx, "_host", "http://127.0.0.1"),
            port=getattr(ctx, "_port", 8888),
            group=ctx.FromGroupId,
        )
        if ctx.FromUserId not in admins:
            return func(ctx)
        return None

    return inner
