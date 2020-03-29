from . import models as us
from django.contrib import admin


class AdminLogin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ['username', 'name', 'email', 'create_time']
    # 搜索框，按照元组内指定字段搜索
    search_fields = ('username', 'name')
    # 按时间过滤
    date_hierarchy = 'create_time'
    # 定义动作列表
    actions = ["publish_status", "withdraw_status"]
    # 每页显示多少条
    list_per_page = 20

    # 禁止登陆动作函数 参数固定
    def publish_status(self, request, queryset):
        queryset.update(is_active=False)

    publish_status.short_description = '冻结用户'  # 指定动作显示名称

    # 允许登陆动作函数 参数固定
    def withdraw_status(self, request, queryset):
        queryset.update(is_active=True)

    withdraw_status.short_description = '解除冻结'  # 指定动作显示名称


class Types(admin.ModelAdmin):
    list_display = ['type']
    search_fields = ('type', )
    list_filter = ['type']
    list_per_page = 20


class BookList(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'publish_time', 'page', 'price', 'score', 'isbn', 'create_time']
    search_fields = ('title', 'isbn')
    date_hierarchy = 'create_time'
    list_per_page = 20


class ShortComment(admin.ModelAdmin):
    list_display = ['user', 'book', 'content', 'create_time']
    search_fields = ('content',)
    date_hierarchy = 'create_time'
    list_per_page = 20


class LongComment(admin.ModelAdmin):
    list_display = ['user', 'book', 'content', 'create_time']
    search_fields = ('content',)
    date_hierarchy = 'create_time'
    list_per_page = 20


# 注册   第一个参数为数据库模型， 第二为自己写的类
admin.site.register(us.User, AdminLogin)
admin.site.register(us.Type, Types)
admin.site.register(us.Books, BookList)
admin.site.register(us.Short, ShortComment)
admin.site.register(us.Long, LongComment)

