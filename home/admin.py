from django.contrib import admin
from .models import *

@admin.register(Message)
class PostAdmin(admin.ModelAdmin):      
    list_display = ('id', 'user', 'message', 'created')
    # search_fields = ('user',)
