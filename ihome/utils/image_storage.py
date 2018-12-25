from qiniu import Auth, etag, put_data
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'YV0d_2cEZhKNmwB3rL-DdcHIBiSuLdQEiGsU34oG'
secret_key = 'NkFytLJdAkxZEtICVwfMN366TW5sZI6EdlnTfZOI'


def storage(file_data):
    """
    上传文件到七牛云
    :param file_data: 要上传的文件数据
    """
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'ihome'

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    ret, info = put_data(token, None, file_data)

    print(info)
    print("*"*10)
    print(ret)
