from django.contrib import admin
from .models import Note, Tag, UploadedImage

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_pinned', 'is_deleted', 'created_at', 'updated_at']
    list_filter = ['is_pinned', 'is_deleted', 'user', 'created_at']
    search_fields = ['title', 'content', 'user__username']
    filter_horizontal = ['tags']

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'uploaded_at']
    list_filter = ['user', 'uploaded_at']
    search_fields = ['user__username']
