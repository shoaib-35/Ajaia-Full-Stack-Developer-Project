from django.contrib import admin

from .models import Document, DocumentShare, UploadedFile


admin.site.register(Document)
admin.site.register(DocumentShare)
admin.site.register(UploadedFile)
