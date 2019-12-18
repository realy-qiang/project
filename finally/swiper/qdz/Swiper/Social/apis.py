from django.shortcuts import render

# Create your views here.
from Social import logics
from libs.http import render_json
from common.stat import LogicError
from user.models import User
from vip.logics import require_permission
from Social.models import Friend



def rcmd_users(request):
    '''推荐用户接口'''
    users = logics.rcmd(request.uid)
    rcmd_data = [user.to_dict() for user in users]
    return render_json(rcmd_data)


def like(request):
    '''喜欢/右滑'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched':is_matched})

@require_permission('superlike')
def superlike_someone(request):
    '''超级喜欢/上滑'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched':is_matched})


def dislike_someone(request):
    '''不喜欢/左滑'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    
    return render_json()

@require_permission('rewind')
def rewind(request):
    '''
    反悔操作
    传参处理的原则：
        1、客户端传来的任何的东西都不可信
        2、所有客户端传来的信息都需要进行验证
        3、能不依赖客户端的数据尽量不让客户端传
    '''
    logics.rewind_swiper(request.uid)
    return render_json()

@require_permission('who_like_me')
def who_liked_me(request):
    '''查看谁喜欢过自己'''
    users = logics.user_liked_me(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)

def friend_list(request):
    '''查看自己的好友列表'''
    fid_list = Friend.friend_id_list(request.uid)
    users = User.objects.filter(id__in=fid_list)
    friends = [user.to_dict() for user in users]
    return render_json(friends)

def hot_rank(request):
    '''查看人气排行榜'''
    rank_data = logics.get_top_n(50)
    return render_json(rank_data)