from django.urls import path

from .views import (
    compare_versions,
    create_or_edit_document,
    delete_document,
    view_document,
    document_list,
)


urlpatterns = [
    path('', document_list, name='document_list'),
    path('create/', create_or_edit_document, name='create_document'),
    path('<int:document_id>/', view_document, name='view_document'),
    path('<int:document_id>/edit/', create_or_edit_document,
         name='edit_document'),
    path('<int:document_id>/delete/', delete_document, name='delete_document'),
    path('<int:document_id>/compare/', compare_versions,
         name='compare_versions'),
]
