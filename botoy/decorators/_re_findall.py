import re
from typing import Union

from ..model import FriendMsg, GroupMsg


def re_findall(pattern: Union[str, re.Pattern]):
    """正则匹配Content字段 GroupMsg, FriendMsg
    因为使用这种功能一般匹配的内容都比较特殊,像图片，视频之类的消息基本是不会符合匹配条件的,
    所以不会解析特殊的消息, 均采用最原始的Content字段进行匹配,

    匹配使用的是`re.findall`方法，匹配结果可通过`ctx._findall`属性调用

    :param pattern: 正则表达式
    """

    def deco(func):
        def inner(ctx):
            assert isinstance(ctx, (GroupMsg, FriendMsg))
            find = re.findall(pattern, ctx.Content)
            if find:
                setattr(ctx, "_findall", find)
                return func(ctx)
            return None

        return inner

    return deco
