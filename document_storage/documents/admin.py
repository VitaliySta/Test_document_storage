from django.contrib import admin

from .models import Document, DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'is_deleted',
        'current_version',
    )
    search_fields = (
        'name',
    )


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'document',
        'content',
        'created_at',
    )
    list_filter = (
        'document',
        'created_at',
    )
    search_fields = (
        'document',
        'content',
    )
