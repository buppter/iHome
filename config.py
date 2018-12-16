class Config():
    """配置信息"""

    SECRET_KEY = 'dfasaf23432sfa083jafd1faszza'

    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@10.112.214.168:3306/ihome'

    # redis
    REDIS_HOST = '10.112.214.168'
    REDIS_PORT = 6379

    # flask_session 配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # session的有效期，单位秒


class DevelopmentConfig(Config):
    """开发环境的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境的配置信息"""
    pass


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}