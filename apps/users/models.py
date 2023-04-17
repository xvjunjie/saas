from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserInfo(AbstractUser):
    #1代表是管理员;0代表是普通用户
    user_no = models.CharField(max_length=50, verbose_name='学号/工号')
    is_admin = models.IntegerField(default=0, verbose_name="用户类型", help_text="用户类型")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间", help_text="创建时间")
    is_delete = models.BooleanField(default=False, verbose_name='是否删除', help_text="是否删除")

    class Meta:
        db_table = 'tb_user_info'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Course(models.Model):
    course_name = models.CharField(max_length=30, verbose_name='课程名称')

    class Meta:
        db_table = 'tb_course'
        verbose_name = '课程表'

    def __str__(self):
        return self.course_name

class Record(models.Model):
    user_no = models.CharField(max_length=50)
    course_id = models.IntegerField(verbose_name='课程id')
    course_name = models.CharField(max_length=30, verbose_name='课程名')
    grade = models.IntegerField(default=60, verbose_name='分数')
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        db_table = 'tb_record'
        verbose_name = '成绩表'

    def __str__(self):
        return self.course_name
