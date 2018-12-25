import json

from flask import current_app, jsonify

from ihome import redis_store, constants
from ihome.api_1_0 import api
from ihome.models import Area
from ihome.utils.response_code import RET


@api.route("/areas")
def get_area_info():
    """
    获取城区信息
    :return:
    """
    # 尝试从redis中读取数据
    try:
        resp_json = redis_store.get("area_info")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            # 表示redis中有缓存数据
            return resp_json, 200, {"Content-Type": "application/json"}

    # 如果redis中没有缓存，则进行查询数据库，读取城区信息
    try:
        area_list = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    area_dict = []
    # 将对象转换为字典
    for area in area_list:
        area_dict.append(area.to_dict())

    # 将数据转换为json字符串
    resp_dict = dict(errno=RET.OK, errmsg="OK", data=area_dict)
    resp_json = json.dumps(resp_dict)

    # 将数据保存到redis中
    try:
        redis_store.setex("area_info", constants.AREA_INFO_REDIS_CACHE_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)

    return resp_json, 200, {"Content-Type": "application/json"}
