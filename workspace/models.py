from django.conf import settings
from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=200, default="Untitled document")
    content = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_documents",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class DocumentShare(models.Model):
    VIEWER = "viewer"
    EDITOR = "editor"
    ROLE_CHOICES = [
        (VIEWER, "Viewer"),
        (EDITOR, "Editor"),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="shares",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="document_shares",
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=VIEWER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document", "user"],
                name="unique_document_share",
            )
        ]


class UploadedFile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files",
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="source_files",
    )
    original_name = models.CharField(max_length=255)
    file_data = models.BinaryField()
    file_size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
