'''邮箱验证配置'''

# 云之讯短信验证配置
# YZX_SMS_API = 'https://open.ucpaas.com/ol/sms/sendsms'
# YZX_SMS_ARGS = {
#     "sid": "2ff56f07e2d002ab9900777dd4b09edf",
#     "token": "d763718424035afc347cbd3bba3813a2",
#     "appid": "8235102f41ed4603802b05264c59430e",
#     "templateid": "503617",
#     "param": None,
#     "mobile": None,
# }

# 千牛云
QN_AK = 'NGoGXcMFKqdsjhKdFZUVjqblgN6NAkMW05YKr3ji'
QN_SK = 'Zcujb8Kd4_q0EqLflxqF-jw2ZHpdlx7knnk_cZyS'
QN_BUCKET_NAME = 'jiangang'
QN_BASE_URL = 'http://q1pv1vd9u.bkt.clouddn.com'

# redis配置
REDIS = {
	'host' : 'localhost',
	'port' : 6379,
	'db' : 5,
}

# 反悔设置
REWIND_TIMES = 3  # 每天反悔次数
REWIND_TIMEOUT = 60 * 5  # 反悔的超时时间

# 热度积分对应表
HOT_RANK_SCORE = {
	'superlike':7,
	'like':5,
	'dislike':-5
}