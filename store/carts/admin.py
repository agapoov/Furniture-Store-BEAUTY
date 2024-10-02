from carts.models import Cart
from django.contrib import admin

# admin.site.register(Cart)


class CartTableAdmin(admin.TabularInline):
    model = Cart
    fields = ('product', 'quantity', 'created_timestamp',)
    search_fields = ('product', 'quantity', 'created_timestamp',)
    readonly_fields = ('created_timestamp',)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('display_username', 'product', 'quantity', 'created_timestamp',)
    list_filter = ('created_timestamp', 'user', 'product__name',)

    def display_username(self, obj):
        return obj.user.username if obj.user and obj.user.is_authenticated else '<Не зарегистрированный>'
