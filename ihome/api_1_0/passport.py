import re

from flask import request, jsonify, current_app

from ihome import redis_store
from ihome.utils.response_code import RET
from . import api


@api.route("/users", methods=["POST"])
def register():
    """
    注册
    参数： 手机号，短信验证码，密码，确认密码
    参数格式：json
    """

    # 获取请求的参数，返回字典
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("mobile")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")

    # 校验参数
    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断手机号格式
    if not re.match('1[34578]\d{9}', mobile):
        # 格式不对
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")

    # 业务逻辑处理
    # 从Redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取真实短信验证码异常")
    # 判断短信验证码是否过期
    # 判断用户填写的短信验证码的正确性
    # 判断用户的手机号是否已被注册
    # 保存用户的注册数到数据库中
    # 保存登陆状态到session中
    # 返回结果
