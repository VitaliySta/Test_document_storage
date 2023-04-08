from django.shortcuts import get_object_or_404, redirect, render

from .models import Document, DocumentVersion


def create_document(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')

        if Document.objects.filter(name=name) or not name:
            context = {
                'error': f'Error - Document named {name} exists!'
            }
            return render(request, 'documents/create_document.html', context)

        document = Document(name=name)
        current_version = DocumentVersion(document=document, content=content)
        document.save()
        current_version.save()
        return redirect('view_document', document_id=document.id)
    return render(request, 'documents/create_document.html')


def view_document(request, document_id):

    document = get_object_or_404(Document, id=document_id)
    current_version = DocumentVersion.objects.filter(document=document).latest(
        'created_at'
    )
    context = {
        'document': document,
        'current_version': current_version,
    }
    return render(request, 'documents/view_document.html', context)


def edit_document(request, document_id):

    document = get_object_or_404(Document, id=document_id)
    current_version = DocumentVersion.objects.filter(document=document).latest(
        'created_at'
    )
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')

        if document.name != name:

            if Document.objects.filter(name=name) or not name:
                context = {
                    'document': document,
                    'current_version': current_version,
                    'error': f'Error - Document named {name} exists!',
                }
                return render(request, 'documents/edit_document.html', context)

            document.name = name
            document.save()

        if current_version.content != content:
            doc = DocumentVersion(document=document, content=content)
            doc.save()

        return redirect('view_document', document_id=document.id)
    context = {
        'document': document,
        'current_version': current_version,
    }
    return render(request, 'documents/edit_document.html', context)


def delete_document(request, document_id):

    document = Document.objects.get(id=document_id)
    document.is_deleted = True
    document.save()
    return redirect('view_document', document_id=document.id)


def compare_versions(request, document_id):

    document = Document.objects.get(id=document_id)
    doc_versions = DocumentVersion.objects.filter(document=document)
    current_version = doc_versions.latest('created_at')
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
