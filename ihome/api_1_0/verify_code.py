from . import api
from ihome.utils.captcha.captcha import captcha

# 127.0.0.1:5000/api/v1.0/image_codes/<image_code_id>


@api.route('/image_code/<string:image_code_id>')
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return 验证码图片
    """
    # 业务逻辑处理
    # 生成验证码图片
    # 名字， 真实文本， 图片数据
    name, text, image_data = captcha.generate_captcha()

    # 将验证码真实值与编号保存到redis中, 设置有效期
    # redis:   字符串  列表  哈希  set
    # "key": xxx
    # 返回值
