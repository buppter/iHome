from . import api


@api.route('/get_image_code')
def get_image_code():
    """
    获取图片验证码
    :return 验证码图片
    """
