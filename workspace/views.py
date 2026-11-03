import json
import html
from io import BytesIO
from pathlib import Path
from urllib.parse import quote

import markdown
from docx import Document as DocxDocument
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProfileForm, ShareForm, SignUpForm
from .models import Document, DocumentShare, UploadedFile
from .services import clean_document_html, require_access

User = get_user_model()

MAX_UPLOAD_SIZE = 5 * 1024 * 1024
ALLOWED_UPLOAD_EXTENSIONS = {".txt", ".md", ".docx"}


@login_required
def dashboard(request):
    owned_documents = Document.objects.filter(owner=request.user)
    shared_documents = (
        Document.objects.filter(shares__user=request.user)
        .select_related("owner")
        .distinct()[:8]
    )
    shared_entries = [
        (document, document.shares.get(user=request.user))
        for document in shared_documents
    ]

    return render(
        request,
        "workspace/dashboard.html",
        {
            "owned": owned_documents,
            "shared": shared_documents,
            "shared_entries": shared_entries,
        },
    )


@login_required
@require_POST
def create_document(request):
    document = Document.objects.create(
        owner=request.user,
        title="Untitled document",
    )
    return redirect("document_detail", pk=document.pk)


@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    role = require_access(request.user, document)
    shares = (
        document.shares.select_related("user").all()
        if role == "owner"
        else []
    )

    return render(
        request,
        "workspace/editor.html",
        {
            "document": document,
            "role": role,
            "can_edit": role in ("owner", "editor"),
            "shares": shares,
            "safe_content": clean_document_html(document.content),
        },
    )


@login_required
@require_POST
def document_save(request, pk):
    document = get_object_or_404(Document, pk=pk)
    require_access(request.user, document, edit=True)

    try:
        payload = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON")

    content = payload.get("content")
    if not isinstance(content, str) or len(content) > 1_000_000:
        return HttpResponseBadRequest(
            "Invalid or oversized document content"
        )

    document.content = clean_document_html(content)
    document.save(update_fields=["content", "updated_at"])

    return JsonResponse(
        {
            "ok": True,
            "saved_at": document.updated_at.isoformat(),
        }
    )


@login_required
@require_POST
def document_rename(request, pk):
    document = get_object_or_404(Document, pk=pk)
    require_access(request.user, document, owner=True)

    title = request.POST.get("title", "").strip()
    if not title or len(title) > 200:
        messages.error(
            request,
            "Please enter a title between 1 and 200 characters.",
        )
    else:
        document.title = title
        document.save(update_fields=["title", "updated_at"])
        messages.success(request, "Document renamed.")

    return redirect("document_detail", pk=pk)


@login_required
@require_POST
def document_share(request, pk):
    document = get_object_or_404(Document, pk=pk)
    require_access(request.user, document, owner=True)

    form = ShareForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Enter a valid username and permission.")
        return redirect("document_detail", pk=pk)

    target_user = User.objects.filter(
        username__iexact=form.cleaned_data["username"]
    ).first()

    if target_user is None:
        messages.error(request, "No account found with that username.")
    elif target_user == request.user:
        messages.error(request, "You already own this document.")
    else:
        DocumentShare.objects.update_or_create(
            document=document,
            user=target_user,
            defaults={"role": form.cleaned_data["role"]},
        )
        messages.success(
            request,
            f"Document shared with {target_user.username}.",
        )

    return redirect("document_detail", pk=pk)


@login_required
@require_POST
def document_revoke(request, pk, user_id):
    document = get_object_or_404(Document, pk=pk)
    require_access(request.user, document, owner=True)

    DocumentShare.objects.filter(
        document=document,
        user_id=user_id,
    ).delete()
    messages.success(request, "Access removed.")

    return redirect("document_detail", pk=pk)


@login_required
@require_POST
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    require_access(request.user, document, owner=True)

    document.delete()
    messages.success(request, "Document deleted.")

    return redirect("dashboard")


@login_required
def shared_documents(request):
    documents = (
        Document.objects.filter(shares__user=request.user)
        .select_related("owner")
        .distinct()
    )
    entries = [
        (document, document.shares.get(user=request.user))
        for document in documents
    ]

    return render(
        request,
        "workspace/shared.html",
        {"entries": entries},
    )


@login_required
def files_page(request):
    uploaded_files = UploadedFile.objects.filter(owner=request.user)
    return render(
        request,
        "workspace/files.html",
        {"files": uploaded_files},
    )


@login_required
@require_POST
def file_upload(request):
    uploaded_file = request.FILES.get("file")
    if uploaded_file is None:
        messages.error(request, "Choose a file to upload.")
        return redirect("files_page")

    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        messages.error(
            request,
            "Supported formats are .txt, .md and .docx.",
        )
        return redirect("files_page")

    if uploaded_file.size > MAX_UPLOAD_SIZE:
        messages.error(request, "File exceeds the 5 MB limit.")
        return redirect("files_page")

    raw_content = uploaded_file.read()

    try:
        document_title = Path(uploaded_file.name).stem

        if extension == ".docx":
            if not raw_content.startswith(b"PK"):
                raise ValueError("Invalid DOCX archive")

            parsed_document = DocxDocument(BytesIO(raw_content))
            text_content = "\n".join(
                paragraph.text for paragraph in parsed_document.paragraphs
            )
            html_content = "".join(
                f"<p>{html.escape(line)}</p>"
                for line in text_content.splitlines()
            )
        else:
            text_content = raw_content.decode("utf-8-sig")

            if extension == ".md":
                html_content = markdown.markdown(
                    text_content,
                    extensions=["extra", "sane_lists"],
                )
            else:
                html_content = "".join(
                    f"<p>{html.escape(line)}</p>"
                    for line in text_content.splitlines()
                )

    except Exception:
        messages.error(
            request,
            "We could not read this file. Check that it is a valid "
            "UTF-8 text, Markdown or DOCX file.",
        )
        return redirect("files_page")

    document = Document.objects.create(
        owner=request.user,
        title=document_title[:200] or "Imported document",
        content=clean_document_html(html_content),
    )
    UploadedFile.objects.create(
        owner=request.user,
        document=document,
        original_name=Path(uploaded_file.name).name[:255],
        file_data=raw_content,
        file_size=len(raw_content),
    )

    messages.success(
        request,
        "File imported and converted into an editable document.",
    )
    return redirect("document_detail", pk=document.pk)


@login_required
def file_download(request, pk):
    uploaded_file = get_object_or_404(
        UploadedFile,
        pk=pk,
        owner=request.user,
    )
    response = HttpResponse(
        bytes(uploaded_file.file_data),
        content_type="application/octet-stream",
    )
    response["Content-Disposition"] = (
        f"attachment; filename*=UTF-8''{quote(uploaded_file.original_name)}"
    )
    response["X-Content-Type-Options"] = "nosniff"

    return response


@login_required
@require_POST
def file_delete(request, pk):
    uploaded_file = get_object_or_404(
        UploadedFile,
        pk=pk,
        owner=request.user,
    )
    uploaded_file.delete()
    messages.success(
        request,
        "Uploaded file deleted. The imported document remains available.",
    )

    return redirect("files_page")


@login_required
def account_settings(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("account_settings")
    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "workspace/settings.html",
        {"form": form},
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account is ready. Welcome to Ajaia Docs!",
            )
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form},
    )
