from django.utils.deprecation import MiddlewareMixin

import logging
from common import stat
from libs.http import render_json


err_log = logging.getLogger('err')


class AuthMiddleware(MiddlewareMixin):
    path_white_list = [
        '/user/get_code/',
        '/user/submit_code/',
    ]
    '''用户登录验证中间件'''

    def process_request(self, request):

        # 检查当前路径是否在白名单中
        if request.path not in self.path_white_list:
            uid = request.session.get('uid', 1)
            print(uid)
            if not uid:
                return render_json(code=stat.LoginRequired.code)
            else:
                request.uid = uid


class LogicErrMiddleware(MiddlewareMixin):
    """逻辑异常处理中间件"""
    def process_exception(self, request, exception):
        if isinstance(exception, stat.LogicError):
            return render_json(exception.data,exception.code)
        
