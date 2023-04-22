from django.contrib import admin
from .models import PostCategory

# Register your models here.

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    fields = ('name',)