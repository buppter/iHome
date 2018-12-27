import random

from flask import current_app, jsonify, make_response, request

from ihome import redis_store, constants, db
from ihome.models import User
from ihome.utils.YunPian import Yunpian
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
from ihome.tasks.sms.tasks import send_sms


# 127.0.0.1:5000/api/v1.0/image_codes/<image_code_id>
@api.route('/image_code/<string:image_code_id>')
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return 正常：返回验证码图片  异常：返回json
    """
    # 业务逻辑处理
    # 生成验证码图片
    # 名字， 真实文本， 图片数据
    name, text, image_data = captcha.generate_captcha()

    # 将验证码真实值与编号保存到redis中, 设置有效期
    # redis:   字符串  列表  哈希  set
    # "key": xxx

    # 使用哈希维护有效期的时候只能整体设置
    # image_codes:

    # 单条维护记录，选用字符串
    # "image_codes_编号1": "真实值"
    # "image_codes_编号2": "真实值"

    # redis_store.set("image_code_%s" % image_code_id, text)
    # redis_store.expire("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)
    try:
        #                                         记录名字      有效期                            文本
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)

        # return jsonify(error=RET.DBERR, errormsg="save image code failed")
        return jsonify(error=RET.DBERR, errormsg="保存图片验证码信息失败")

    # 返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxx&image_code_id=xxx
# @api.route("/sms_codes/<re('1[34578]\d{9}'):mobile>")
# def get_sms_code(mobile):
#     """
#     获取短信验证码
#     :param mobile 手机号，sms_code 短信验证码
#     :return sms_status 0表示发送成功
#     """
#     # 获取参数
#     image_code = request.args.get("image_code")
#     image_code_id = request.args.get("image_code_id")
#
#     # 校验参数
#     if not all([image_code, image_code_id]):
#         # 表示参数不完整
#         return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
#
#     # 业务逻辑处理
#
#     # 从Redis中取出真实的图片验证码
#     try:
#         real_image_code = redis_store.get("image_code_%s" % image_code_id)
#
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="Redis数据库异常")
#
#     # 判断图片验证码是否过期
#     if real_image_code is None:
#         # 表示图片验证码过期或者没有
#         return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")
#
#     # 删除Redis中的图片验证码，防止用户使用同一个图片验证码验证多次
#     try:
#         redis_store.delete("image_code_%s" % image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#
#     # 与用户填写的值进行对比
#     if str(real_image_code, encoding='utf-8').lower() != image_code.lower():
#
#         # 表示用户填写错误
#         return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")
#
#     # 判断对于当前手机号的操作在60秒内是否有记录。如果有，则认为用户频繁操作，不接收处理
#     try:
#         send_flag = redis_store.get("send_sms_code_%s" % mobile)
#     except Exception as e:
#         current_app.logger.error(e)
#     else:
#         if send_flag is not None:
#             # 表示60秒内之前有过发送的记录
#             return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60后重试")
#
#     # 判断手机号是否已被注册
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except Exception as e:
#         current_app.logger.error(e)
#     else:
#         if user is not None:
#             # 表示手机号已经存在
#             return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
#
#     # 如果未被注册，则生成短信验证码
#     sms_code = "%06d" % random.randint(0, 999999)
#
#     # 保存真实的短信验证码
#     try:
#         redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
#         # 保存发送给当前手机号的记录，防止用户60秒内再次发送短信
#         redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="短信验证码异常")
#
#     # 发送短信
#     try:
#         yun_pian = Yunpian(constants.API_KEY)
#         # sms_status = yun_pian.send_sms(code=sms_code, mobile=mobile)
#         sms_status = 0
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.THIRDERR, errmsg="发送异常")
#
#     # 返回值
#     if sms_status == 0:
#         # 发送成功
#         return jsonify(errno=RET.OK, errmsg="发送成功")
#     else:
#         return jsonify(errno=RET.THIRDERR, errmsg=sms_status["msg"])


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxx&image_code_id=xxx
@api.route("/sms_codes/<re('1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """
    获取短信验证码
    :param mobile 手机号，sms_code 短信验证码
    :return sms_status 0表示发送成功
    """
    # 获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    # 校验参数
    if not all([image_code, image_code_id]):
        # 表示参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 业务逻辑处理

    # 从Redis中取出真实的图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="Redis数据库异常")

    # 判断图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码过期或者没有
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除Redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 与用户填写的值进行对比
    if str(real_image_code, encoding='utf-8').lower() != image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断对于当前手机号的操作在60秒内是否有记录。如果有，则认为用户频繁操作，不接收处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if send_flag is not None:
            # 表示60秒内之前有过发送的记录
            return jsonify(errno=RET.REQERR, errmsg="请求过于频繁，请60后重试")

    # 判断手机号是否已被注册
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已经存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果未被注册，则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)

    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给当前手机号的记录，防止用户60秒内再次发送短信
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="短信验证码异常")

    # 发送短信
    # 使用celery异步发送短信，delay函数调用后立即返回
    sms_result = send_sms.delay(mobile, sms_code).get()

    sms_status = sms_result.get("code")

    # 返回值
    if sms_status == 0:
        # 发送成功
        return jsonify(errno=RET.OK, errmsg="发送成功")
    else:
        return jsonify(errno=RET.THIRDERR, errmsg=sms_result["msg"])
