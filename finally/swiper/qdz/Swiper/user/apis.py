# import os
import logging

from django.core.cache import cache

from libs.http import render_json
from common import stat
from common import keys
from user import logics
from user.form import ProfileForm
from user.form import UserFrom
from user.logics import send_code_email
from user.models import User, Profile
from libs.cache import rds


inf_log = logging.getLogger('inf')


def get_code(request):
    '''
    获取验证码
    :param request:
    :return:
    '''
    email = request.GET.get('email')
    print(email)
    send_status = send_code_email(email)
    if send_status:
        return render_json()
    else:
        raise stat.SendEmailErr


def submit_code(request):
    '''
    登录注册
    :param request:
    :return:
    '''
    email = request.POST.get('email')
    input_code = request.POST.get('code')
    code = cache.get('e_code' + email)
    if code == input_code and input_code:
        try:
            user = User.objects.get(email=email)
            inf_log.info('%s login with id %s' % (user.nickname, user.id))
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            inf_log.info('new user: %s' % user.id)

        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        raise stat.VcodeErr


def get_profile(request):
    '''获取个人资料'''

    key = keys.PROFILE_KEY % request.uid
    result = rds.get(key)
    print('从缓存获取:%s' % result)
    if result is None:
        profile, _ = Profile.objects.get_or_create(id=request.uid)
        result = profile.to_dict()
        rds.set(key, result, 1000)  # 将数据写入到缓存中

    return render_json(result)


def set_profile(request):
    '''修改个人资料'''
    user_form = UserFrom(request.POST)
    profile_form = ProfileForm(request.POST)

    

    if not user_form.is_valid():
        print(user_form.errors)
        raise stat.UserFormErr(user_form.errors)

    if not profile_form.is_valid():
        raise stat.ProfileFormErr(profile_form.errors)

    # 保存数据
    User.objects.filter(id=request.uid).update(**user_form.cleaned_data)
    Profile.objects.filter(id=request.uid).update(**profile_form.cleaned_data)

    # 数据修改过后删除旧的缓存
    key = keys.PROFILE_KEY % request.uid
    rds.delete(key)
    return render_json()


def upload_avatar(request):
    '''
        头像上传
        1.将文件保存到本地
        2.从本地上传至七牛云
        3.保存 URL
        4.删除本地文件
    '''

    avatar_file = request.FILES.get('avatar')
    # logics.save_avatar.delay(request.uid, avatar_file)
    # avatar_url = upload_to_qiniu(filename, filepath)
    # User.objects.filter(id=request.uid).update(avatar_url)
    # os.remove(filepath)
    logics.upload_avatar(request.uid, avatar_file)
    return render_json()
