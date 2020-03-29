from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # 用户名/密码/邮箱 为默认
    name = models.TextField(verbose_name='用户昵称')
    image = models.ImageField(upload_to='Image', verbose_name='用户头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    code = models.TextField(verbose_name='验证码')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息管理'
        verbose_name_plural = verbose_name


class Type(models.Model):
    # 图书类型做主键,便于筛选
    type = models.TextField(verbose_name='图书类型')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = '图书分类管理'
        verbose_name_plural = verbose_name


class Books(models.Model):
    # 图书封面存为URL
    title = models.TextField(verbose_name='图书名称')
    image = models.TextField(verbose_name='图书封面')
    author = models.TextField(verbose_name='图书作者')
    publish = models.TextField(verbose_name='出版社')
    publish_time = models.TextField(verbose_name='出版时间')
    page = models.IntegerField(verbose_name='图书页数')
    price = models.FloatField(verbose_name='图书定价')
    score = models.FloatField(verbose_name='图书评分')
    content = models.TextField(verbose_name='图书简介')
    isbn = models.TextField(verbose_name='图书ISBN')
    type = models.ForeignKey("Type", null=True, blank=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '图书详情管理'
        verbose_name_plural = verbose_name


class State(models.Model):
    # 用户状态：0为想读,1为在读,2为读过
    user = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)
    book = models.IntegerField(verbose_name='图书编号')
    state = models.IntegerField(verbose_name='用户状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '用户状态管理'
        verbose_name_plural = verbose_name


class Short(models.Model):
    user = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)
    book = models.IntegerField(verbose_name='图书编号')
    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '图书短评管理'
        verbose_name_plural = verbose_name


class Long(models.Model):
    user = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)
    book = models.IntegerField(verbose_name='图书编号')
    content = models.TextField(verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '图书长评管理'
        verbose_name_plural = verbose_name


class Photo(models.Model):
    long = models.ForeignKey("Long", null=True, blank=True, on_delete=models.SET_NULL)
    photo = models.ImageField(upload_to='Photo', verbose_name='用户头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user
