from django.urls import path

from . import views


urlpatterns = [
    path("accounts/signup/", views.signup, name="signup"),
    path("", views.dashboard, name="dashboard"),
    path("documents/create/", views.create_document, name="document_create"),
    path(
        "documents/<int:pk>/",
        views.document_detail,
        name="document_detail",
    ),
    path(
        "documents/<int:pk>/save/",
        views.document_save,
        name="document_save",
    ),
    path(
        "documents/<int:pk>/rename/",
        views.document_rename,
        name="document_rename",
    ),
    path(
        "documents/<int:pk>/share/",
        views.document_share,
        name="document_share",
    ),
    path(
        "documents/<int:pk>/revoke/<int:user_id>/",
        views.document_revoke,
        name="document_revoke",
    ),
    path(
        "documents/<int:pk>/delete/",
        views.document_delete,
        name="document_delete",
    ),
    path("shared/", views.shared_documents, name="shared_documents"),
    path("files/", views.files_page, name="files_page"),
    path("files/upload/", views.file_upload, name="file_upload"),
    path(
        "files/<int:pk>/download/",
        views.file_download,
        name="file_download",
    ),
    path("files/<int:pk>/delete/", views.file_delete, name="file_delete"),
    path("settings/", views.account_settings, name="account_settings"),
]
