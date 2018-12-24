import re

from flask import request, jsonify, current_app, session
from sqlalchemy.exc import IntegrityError

from ihome import redis_store, db, constants
from ihome.models import User
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
    sms_code = req_dict.get("sms_code")
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
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码已失效")

    # 删除Redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    # 判断用户填写的短信验证码的正确性
    if str(real_sms_code, encoding="utf-8") != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    # 判断用户的手机号是否已被注册
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    #
    # else:
    #     if user is not None:
    #         # 表示手机号已经存在
    #         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 保存用户的注册数到数据库中
    user = User(
        name=mobile,
        mobile=mobile,
    )

    user.password = password  # 设置属性

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()

        # 表示手机号出现了重复值,即手机号已经注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    # 保存登陆状态到session中
    session['name'] = mobile
    session['mobile'] = mobile
    session['user_id'] = user.id

    # 返回结果
    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route("/sessions", methods=["POST"])
def login():
    """
    用户登陆
    参数：手机号，密码  json
    :return:
    """
    # 获取参数
    req_dict = request.get_json()
    print(req_dict)
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    # 校验参数

    # 参数完整的校验
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 手机号的格式
    if not re.match('1[34578]\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不完整")

    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： "access_nums_请求的IP": 次数
    user_ip = request.remote_addr  # 用户的IP
    try:
        access_nums = redis_store.get("access_nums_%s" % user_ip)
        print(int(access_nums))
    except Exception as e:
        current_app.logger.error(e)
    else:
        print(int(access_nums), type(access_nums))
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            print(access_nums, int(access_nums))
            return jsonify(errno=RET.REQERR, errmsg="错误请求次数过多，请稍后重试")

    # 从数据库中根据手机号查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or not user.check_password(password):
        # 如果校验失败，记录错误次数，返回信息
        try:
            redis_store.incr("access_nums_%s" % user_ip)
            redis_store.expire("access_nums_%s" % constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

    # 如果验证通过，保存登陆状态，在session中
    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id
    return jsonify(errno=RET.OK, errmsg="登陆成功")


@api.route("/session", methods=["GET"])
def check_loign():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登陆，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="True", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="False")


@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session中的数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")
