from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'completed', 'created_at', 'due_date']
    list_filter = ['completed', 'priority', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['completed']
