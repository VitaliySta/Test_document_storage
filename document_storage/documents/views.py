from django.shortcuts import get_object_or_404, redirect, render

from .models import Document, DocumentVersion


def create_or_edit_document(request, document_id=None):

    document = None
    current_version = None

    if document_id:
        document = get_object_or_404(Document, id=document_id)
        current_version = DocumentVersion.objects.filter(
            document=document).latest('created_at')

    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')

        if not name or Document.objects.filter(name=name).exclude(
                id=document_id).exists():
            context = {
                'document': document,
                'current_version': current_version,
                'error': f'Error - Document named {name} exists!',
            }
            return render(request, 'documents/edit_document.html', context)

        if document_id:
            document.name = name
            document.save()
        else:
            document, _ = Document.objects.get_or_create(name=name)

        if current_version is None or current_version.content != content:
            current_version = DocumentVersion.objects.create(
                document=document, content=content)
            document.current_version = current_version
            document.save()

        return redirect('view_document', document_id=document.id)

    if document_id:
        context = {
            'document': document,
            'current_version': current_version,
        }
        return render(request, 'documents/edit_document.html', context)
    return render(request, 'documents/create_document.html')


def view_document(request, document_id):

    document = get_object_or_404(Document, id=document_id)
    context = {
        'document': document,
    }
    return render(request, 'documents/view_document.html', context)


def delete_document(request, document_id):

    document = Document.objects.get(id=document_id)
    document.is_deleted = True
    document.save()
    return redirect('view_document', document_id=document.id)


def compare_versions(request, document_id):

    document = Document.objects.get(id=document_id)
    doc_versions = DocumentVersion.objects.filter(document=document)
    current_version = document.current_version
    if len(doc_versions) > 1:
        previous_version = doc_versions.exclude(id=current_version.id).latest(
            'created_at'
        )
        context = {
            'current_version': current_version.created_at,
            'previous_version': previous_version.created_at,
            'current_content': current_version.content,
            'previous_content': previous_version.content,
        }
        return render(request, 'documents/compare_versions.html', context)
    context = {
        'current_version': current_version.created_at,
        'previous_version': None,
    }
    return render(request, 'documents/compare_versions.html', context)


def document_list(request):

    documents = Document.objects.filter(is_deleted=False)
    context = {
        'documents': documents,
    }
    return render(request, 'documents/index.html', context)
