from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.models import Category, Blog, CustomUser, Product

# Register your models here.

@admin.register(Blog)
class BlogInfoAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CustomUser)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    fields = [_('name'), _('price')]

