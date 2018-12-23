import re

from flask import request, jsonify, current_app, session
from sqlalchemy.exc import IntegrityError

from ihome import redis_store, db
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
        print(real_sms_code)
        print(sms_code)
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

    user.password = password    # 设置属性

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
