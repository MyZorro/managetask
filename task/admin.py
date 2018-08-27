from django.contrib import admin
from task.models import Person, Product


class PersonAdmin(admin.ModelAdmin):
    list_display = ['person_name', 'position', 'email', 'modify_time', 'status']
    search_fields = ['person_name']
    list_filter = ['status']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['Product_name', 'Product_describe', 'status']
    search_fields = ['Product_name']
    list_filter = ['status']


admin.site.register(Person, PersonAdmin)
admin.site.register(Product, ProductAdmin)
