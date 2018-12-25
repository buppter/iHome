import functools

from flask import session, jsonify, g
from werkzeug.routing import BaseConverter


# 定义正则转换器
from ihome.utils.response_code import RET


class ReCoverter(BaseConverter):
    """"""

    def __init__(self, url_map, *args):
        # 调用父类的初始化方法
        super(ReCoverter, self).__init__(url_map)

        # 保存正则表达式
        self.regex = args[0]


# 定义的验证登陆状态的装饰器
def login_required(view_func):

    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登陆状态
        user_id = session.get("user_id")

        # 如果用户是登陆的，执行视图函数
        if user_id is not None:
            # 将user_id保存到g对象中，在视图函数中可以通过g对象获取保存数据
            g.user_id = user_id
            return view_func(*args, **kwargs)

        # 如果未登陆，返回未登录的信息
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登陆")

    return wrapper
