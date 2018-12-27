from ihome import constants
from ihome.tasks.main import celery_app
from ihome.utils.YunPian import Yunpian


@celery_app.task
def send_sms(mobile, sms_code):
    """发送短信的异步任务"""
    yunpian = Yunpian(constants.API_KEY)
    ret = yunpian.send_sms(code=sms_code, mobile=mobile)
    return ret
