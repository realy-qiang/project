# 各种缓存的 LKey
VCOED_K = 'Vcode-%s'  # 验证的key,拼接邮箱号

FIRST_CRMD_K = "FIRST_CRMD_Q-%s"  # 优先推荐队列，拼接uid

REWIND_KEY = "Rewind_%s_%s"  # 反悔次数的key 拼接当天日期和uid

PROFILE_KEY = "Profile-%s" # 个人资料缓存使用的key

MODEL_K = 'Model-%s-%s'  # 所有model缓存的key 使用model类名和主键进行拼接

HOT_RANK_K = 'HotRankBy'  # 热度积分排行榜