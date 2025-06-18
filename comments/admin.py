from django.contrib import admin
from .models import Comment, CommentInteraction


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'page', 'text_preview', 'karma_score', 'timestamp')
    list_filter = ('timestamp', 'karma_score')
    search_fields = ('user__username', 'text', 'page__title')
    readonly_fields = ('karma_score', 'timestamp')
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'


@admin.register(CommentInteraction)
class CommentInteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment', 'reaction', 'timestamp')
    list_filter = ('reaction', 'timestamp')
    search_fields = ('user__username', 'comment__text')
    readonly_fields = ('timestamp',)

