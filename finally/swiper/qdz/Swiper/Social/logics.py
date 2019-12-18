import datetime

from Swiper import config
from common import stat
from Social.models import Swiped
from Social.models import Friend
from user.models import User
from user.models import Profile
from libs.cache import rds
from common import keys


def first_rcmd(uid):
    '''从redis的优先推荐列表中获取要推荐的用户'''
    uid_list = rds.lrange(keys.FIRST_CRMD_K % uid, 0, 19)
    uid_list = [int(uid) for uid in uid_list]  # 将uid_list中的bytes强转成int
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num, exclude_ids=()):
    '''从数据库中获取要推荐的用户'''
    profile, _ = Profile.objects.get_or_create(id=uid)  # 获取用户的交友资料

    today = datetime.date.today()
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    # 取出滑过的人的id
    # values_list 将查询出来的结果整合成一个列表，列表中的元素是元组，通过flat转换成字符串
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)
    exclude_ids = list(exclude_ids) + list(sid_list)
    
    # 取出需要的用户，同时排除已经滑过的用户
    users = User.objects.filter(
        sex=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday,
    ).exclude(id__in=exclude_ids)[:num]

    return users


def rcmd(uid):
    '''推荐接口'''
    first_user = first_rcmd(uid)  # 首先从优先推荐队列中取出用户
    count = 20 - len(first_user)  # 计算从数据库中取出用户的数量
    first_user_id = [u.id for u in first_user]
    db_user = rcmd_from_db(uid, count, first_user_id)  # 从数据库中取出用户
    # 集合的交集& 并集| 差集 - ，QuerySet支持交集和并集，但是不支持差集
    return list(first_user) + list(db_user)


def like_someone(uid, sid):
    '''喜欢某人'''
    # 添加滑动记录
    Swiped.swiper(uid, sid, 'like')

    # 将sid从自己的优先推荐队列中删除

    rds.lrem(keys.FIRST_CRMD_K % uid, 1, sid)

    # 积分
    score = config.HOT_RANK_SCORE['like']
    print(score)
    # 调整被滑动者的积分
    rds.zincrby(keys.HOT_RANK_K, score, sid)
    print(rds.zrevrange(keys.HOT_RANK_K, 0, 49, withscores=True))


    # 检查对方有没有喜欢自己(右滑或上滑过自己)
    if Swiped.is_liked(sid, uid):
        # 添加好友列表
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢某人'''
    # 添加滑动记录
    Swiped.swiper(uid, sid, 'superlike')

    # 将sid从自己的优先推荐队列中删除
    rds.lrem(keys.FIRST_CRMD_K % uid, 1, sid)

    # 积分
    score = config.HOT_RANK_SCORE['superlike']
    # 调整被滑动者的积分
    rds.zincrby(keys.HOT_RANK_K, score, sid)

    # 检查对方有没有喜欢自己(右滑或上滑过自己)
    liked_me = Swiped.is_liked(sid, uid)
    if liked_me:
        # 添加好友列表
        Friend.make_friends(int(uid), int(sid))
        return True
    elif liked_me == False:
        return False
    else:
        # 对方没有滑动过自己，需要将自己的uid添加到对方的“优先推荐队列”
        rds.rpush(keys.FIRST_CRMD_K % sid, uid)
        return False


def dislike_someone(uid, sid):
    '''不喜欢'''
    Swiped.swiper(uid, sid, 'dislike')

    # 将sid从自己的优先推荐队列中删除
    rds.lrem(keys.FIRST_CRMD_K % uid, 1, sid)

    # 积分
    score = config.HOT_RANK_SCORE['dislike']
    # 调整被滑动者的积分
    rds.zincrby(keys.HOT_RANK_K, score, sid)


def rewind_swiper(uid):
    '''返回一次滑动'''
    # 取出当前时间
    now = datetime.datetime.now()

    # 取出当天的反悔次数
    rewind_k = keys.REWIND_KEY %(now.date(), uid)
    rewind_times = rds.get(rewind_k, 0)  # 当天返回次数，取不到时默认为零

    # 检查当前返回次数
    if rewind_times >= config.REWIND_TIMES:
        raise stat.RewindLimit

    # 取出最后一次的滑动记录
    latest_swiper = Swiped.objects.filter(uid=uid).latest('stime')
    # 检查滑动记录的时间是否超过5分钟
    pass_time = now - latest_swiper.stime
    if pass_time.total_seconds() > config.REWIND_TIMEOUT:
        raise stat.RewindTimeout

    # 如果是超级喜欢，需要将自己从对方的优先推荐队列删除
    if latest_swiper.stype == 'superlike':
        rds.lrem(keys.FIRST_CRMD_K %sid, 1, uid)
        Friend.break_off(uid, latest_swiper.sid)

    # 如果之前是喜欢或超级喜欢 需要撤销好友关系
    elif latest_swiper.stype == 'like':
        Friend.break_off(uid, latest_swiper.sid)


    score = config.HOT_RANK_SCORE[latest_swiper.stype]

    rds.zincrby(keys.HOT_RANK_K, -score, latest_swiper.sid)
    # 将滑动记录删除
    latest_swiper.delete()

    # 更新返回次数
    rds.set(rewind_k, rewind_times +1, 86400)


def user_liked_me(uid):
    '''
    喜欢或者超级喜欢过我的用户
    查询条件：
        - 对方不是自己的好友
        - 我还没有滑动过对方
        - 对方右滑或者上滑过我
    '''
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)
    like_type = ['like', 'superlike']
    uid_list = Swiped.objects.filter(sid=uid,stype__in=like_type).exclude(uid__in=sid_list).values_list('uid', flat=True)
    users = User.objects.filter(id__in=uid_list)
    return users

def get_top_n(num):
    origin_data = rds.zrevrange(keys.HOT_RANK_K, 0, num-1, withscores=True)  # 取出原始排行数据
    print(origin_data)
    cleaned = [[int(uid), int(score)] for uid, score in origin_data]  # 对原始数据进行清洗

    uid_list = [uid for uid, _ in cleaned]  # 取出所有的uid

    users = User.objects.filter(id__in=uid_list)  # 取出所有的用户
    users = sorted(users, key=lambda user: uid_list.index(user.id))  # 对用户进行排序

    rank_data = {}
    for idx, user in enumerate(users):
        score = cleaned[idx][1]
        user_info = user.to_dict('email', 'birthday', 'location', 'vip_id', 'vip_end')
        rank = idx + 1
        rank_data[rank] = user_info

    return rank_data