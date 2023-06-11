from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import *


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cat', 'slug')
    list_display_links = ('title', 'slug', )
    prepopulated_fields = {"slug": ("title",)}


class FoodFilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rest')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'rest', 'cat', 'price', 'get_photo')
    search_fields = ('title', 'cat')

    def get_photo(self, object):
        select = f"<img style='height: 40px;' src='/static/{object.photo}' alt='no photo' /> "
        return mark_safe(select)


class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'food', 'user', 'quantity', 'total', 'rest')
    list_display_links = ('pk', 'food')
    readonly_fields = ('total', 'rest')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'rest', 'user', 'amount', 'orderDate')
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in obj._meta.fields]


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'food', 'order', 'quantity', 'total',)
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in obj._meta.fields]


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Contact Information', {'fields': ('email', 'phone_number', 'current_address',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('last_login', 'date_joined',)


admin.site.register(Location)
admin.site.register(Filter)
admin.site.register(FoodFilter, FoodFilterAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(UserCart, CartAdmin)
admin.site.register(RestLocation)
admin.site.register(Menu, MenuAdmin)
admin.site.register(User, CustomUserAdmin)
