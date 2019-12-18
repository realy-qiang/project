from django.db import models

# Create your models here.
class Vip(models.Model):
	'''会员表'''
	name = models.CharField(max_length=10, unique=True, verbose_name="会员名称")
	level = models.IntegerField(default=0, verbose_name="会员等级")
	price = models.FloatField(default=0.0, verbose_name="会员价格")
	days = models.IntegerField(default=0, verbose_name="天数")


	def has_permission(self, perm_name):
		'''检查当前VIP是否有权限'''
		perm = Permission.objects.get(name=perm_name)
		print(self.id, perm.id)
		return VipPermRelation.objects.filter(vip_id=self.id, perm_id=perm.id).exists()


class Permission(models.Model):
	'''权限表'''
	name = models.CharField(max_length=20, unique=True, verbose_name="权限描述")
	desc = models.TextField(verbose_name="权限描述")


class VipPermRelation(models.Model):
	'''会员权限表'''
	vip_id = models.IntegerField(verbose_name="会员ID")
	perm_id = models.IntegerField(verbose_name="权限ID")