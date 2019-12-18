import os
import random
import time
import logging

from tasks import celery_app
from django.core.cache import cache
from django.core.mail import send_mail

from Swiper import config, settings
# from libs.qn_clond import upload_to_qiniu


from libs.qn_cloud import upload_to_qiniu
from user.models import User

inf_log = logging.getLogger('inf')

def random_code(length=6):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


# def send_vcode(mobile):
#     '''
#     发送短信验证码
#     用户 -> 自己服务器 -> 短信平台 -> 发送短信
#     '''
#     vcode = gen_random_code()  # 产生验证码
#     print('状态码:', vcode)
#
#     args = config.YZX_SMS_ARGS.copy()  # 浅拷贝全局配置
#     args['param'] = vcode
#     args['mobile'] = mobile
#
#     # 调用第三方接口发送验证码
#     response = requests.post(config.YZX_SMS_API, json=args)
#
#     # 检查结果
#     if response.status_code == 200:
#         result = response.json()
#         if result['msg'] == 'OK':
#             cache.set('Vcode-%s' % mobile, vcode, 180)  # 将验证码写入缓存，保存 3 分钟
#             return True
#     return False

# @celery_app.task
def send_code_email(email):
    '''
    发送电子邮箱
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    '''

    email_code = random_code()
    inf_log.debug('状态码: %s' % vcode)

    # args = config.EMAIL_CONFIG.copy()
    email_title = '注册激活'
    email_body = "您的邮箱注册验证码为：{0}， 该验证码有效时间为三分钟，请及时进行验证。".format(email_code)

    receiver = [email]
    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, receiver)

    if send_status:
        cache.set('e_code' + email, email_code, 180)
    return send_status


def save_avatar(uid, avatar_file):
    filename = 'Avatar-%s' % str(uid)
    filepath = '/tmp/%s' % filename
    avatar_url = filepath
    with open(filepath, 'wb') as fp:
        for chunk in avatar_file.chunks():
            fp.write(chunk)

    User.objects.filter(id=uid).update(avatar=avatar_url)

    return filename, filepath

# @celery_app.task
def upload_avatar(uid, avatar_file):
    filename, filepath = save_avatar(uid, avatar_file)
    avatar_url = upload_to_qiniu(filename, filepath)
    User.objects.filter(id=uid).update(avatar=avatar_url)
    os.remove(filepath)
