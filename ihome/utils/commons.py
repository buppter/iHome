from werkzeug.routing import BaseConverter


# 定义正则转换器
class ReCoverter(BaseConverter):
    """"""
    def __init__(self, url_map, *args):

        # 调用父类的初始化方法
        super(ReCoverter, self).__init__(url_map)

        # 保存正则表达式
        self.regex = args[0]


