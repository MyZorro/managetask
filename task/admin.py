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
    list_display = ['Product_name', 'status', 'modify_time', 'create_time']
    search_fields = ['Product_name', 'Product_describe']
    list_filter = ['status', 'create_time']


class PersonInline(admin.StackedInline):
    """用户模块扩展：Person model中的字段将被展示在用户添加中"""
    model = Person
    max_num = 1
    can_delete = False


class PersonAdmin(UserAdmin):
    """扩展哪些东西在用户表"""
    inlines = [PersonInline]
    list_display = ['username', 'email', 'first_name', 'is_staff', 'get_position']

    def get_position(self, positions):
        ps = Person.objects.filter(user_id=positions)
        if ps.exists() is True:
            return ps[0].get_position_display()
        else:
            return '暂未填写'
    get_position.short_description = "职位"
admin.site.unregister(User)
admin.site.register(User, PersonAdmin)
admin.site.register(Product, ProductAdmin)
