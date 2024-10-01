from django.contrib import admin

from .models import Categories, Products

# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name',)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name', 'quantity', 'price', 'discount')
    ordering = ('-quantity',)
    list_editable = ('discount', 'quantity')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    fields = ('name', 'category', 'slug', 'description', 'image', ('price', 'discount'), 'quantity',)
