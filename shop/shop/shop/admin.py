from django.contrib import admin
from shop.shop.models import Shop,ShoppingList, Product, Shoplist_Product
admin.autodiscover()
class ProductInline(admin.TabularInline):
	model = Product
	extra = 4


class Shoplist_ProductAdmin(admin.ModelAdmin):
	inlines = [ProductInline]

admin.site.register(ShoppingList)
admin.site.register(Shoplist_Product, Shoplist_ProductAdmin)


