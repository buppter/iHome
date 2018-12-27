# 图片验证码的Redis有效期,单位 秒
IMAGE_CODE_REDIS_EXPIRES = 180

# 图片验证码的Redis有效期,单位 秒
SMS_CODE_REDIS_EXPIRES = 300

# 发送短信验证码间隔,单位 秒
SEND_SMS_CODE_INTERVAL = 300

# 登陆错误限制次数
LOGIN_ERROR_MAX_TIMES = 5

# 登陆错误限制时间, 单位秒
LOGIN_ERROR_FORBID_TIME = 600

# 云片网API_KEY
API_KEY = '9e2ca7e473cfa3cf36a078fed9f8dba7'

# 七牛云域名
QINIU_URL_DOMAIN = 'http://pkak24rp9.bkt.clouddn.com/'

# 城区信息的缓存时间, 单位：秒
AREA_INFO_REDIS_CACHE_EXPIRES = 7200

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页数据容量
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面页数缓存时间，单位秒
HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES = 7200
