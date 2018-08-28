from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from task.models import Person, Product


# class PersonAdmin(admin.ModelAdmin):
#         '''原来的设计'''
#     list_display = ['person_name', 'position', 'modify_time', 'status']
#     search_fields = ['person_name']
#     list_filter = ['status']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['Product_name', 'Product_describe', 'status']
    search_fields = ['Product_name']
    list_filter = ['status']


class PersonInline(admin.StackedInline):
    """用户模块扩展：Person model中的字段将被展示在用户添加中"""
    model = Person
    max_num = 1
    can_delete = False


class PersonAdmin(UserAdmin):
    """扩展哪些东西在用户表"""
    inlines = [PersonInline]

admin.site.unregister(User)
admin.site.register(User, PersonAdmin)
admin.site.register(Product, ProductAdmin)
