'''
程序状态码
'''

OK = 0


class LogicError(Exception):
	code = None
	data = None

	def __init__(self, data=None):

		self.data = data or self.__class__.__name__


def gen_logic_err(name, code):
	'''封装一个逻辑异常类'''
	return type(name, (LogicError,), {"code":code})


SendEmailErr = gen_logic_err('SendEmailErr', 1000)  #发送短信异常

VcodeErr = gen_logic_err('VcodeErr', 1001)  # 状态码异常

LoginRequired = gen_logic_err('LoginRequired', 1002)  # 用户未登录

UserFormErr = gen_logic_err('UserFormErr', 1003)  # 用户表单错误

ProfileFormErr = gen_logic_err('ProfileFormErr', 1004)  # 资料表单错误

StypeErr = gen_logic_err('StypeErr', 1005)  # 类型错误

ReswiperErr = gen_logic_err('ReswiperErr', 1006)  # 重复滑动

RewindLimit = gen_logic_err('RewindLimit', 1007)  # 超过反悔次数

RewindTimeout = gen_logic_err('RewindLimit', 1008)  # 超过返回时长

VipExpired = gen_logic_err('VipExpired', 1009)  # vip已过期

PermRequired = gen_logic_err('PermRequired', 1010)  # 没有该权限