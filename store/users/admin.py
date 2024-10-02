from carts.admin import CartTableAdmin
from django.contrib import admin
from orders.admin import OrderTabularAdmin

from .models import User

# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',)
    search_fields = ('username', 'first_name', 'last_name', 'email',)

    inlines = [CartTableAdmin, OrderTabularAdmin]
