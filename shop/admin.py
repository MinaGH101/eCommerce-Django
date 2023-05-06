from django.contrib import admin
from .models import *

@admin.register(Product)
class PostAdmin(admin.ModelAdmin):      
    list_display = ('id', 'title', 'category', 'price')
    search_fields = ('title',)
    list_filter = ('created',)
    
    
@admin.register(Seller)
class PostAdmin(admin.ModelAdmin):      
    list_display = ('id', 'product', 'seller')

@admin.register(Promo)
class PostAdmin(admin.ModelAdmin):      
    list_display = ('id', 'code', 'discount')


admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Vote)
admin.site.register(Shipping)


