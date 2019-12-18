# class myIteration(object):
# 	def __iter__(self):
# 		self.x = 0
# 		return self

# 	def __init__(self, n):
# 		self.n = n

# 	def __next__(self):
# 		if self.x < self.n:
# 			self.x += 1
# 			return self.x
# 		else:
# 			raise StopIteration

# my_iteration = myIteration(5)

# for i in my_iteration:
# 	print(i)
import sys


# def fib(n):
# 	a,b, counter = 0, 1, 0
# 	while True:
# 		if counter > n:
# 			return
# 		yield a
# 		a,b = b, a+b
# 		counter += 1
# f = fib(10)

# while True:
# 	try:
# 		print(next(f), end='')
# 	except StopIteration:
# 		sys.exit()

# def fun(val,list=[]):
#     list.append(val)
#     # print(id(list))
#     return list

# data1 = fun(10)
# data2 = fun(123,[])
# data3 = fun('a')

# print(data1)
# print(data2)
# print(data3)

import random

list = [1, 2, 3, 4, 6, 6, 7, 8, 2, 10]
for i in range(3):
    slice = random.sample(list, 5)  # 从list中随机获取5个元素，作为一个片断返回
    print(slice)
    print(list, '\n')  # 原有序列并没有改变