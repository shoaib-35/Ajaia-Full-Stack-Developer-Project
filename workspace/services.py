import bleach
from django.core.exceptions import PermissionDenied

from .models import Document, DocumentShare


ALLOWED_TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    "p",
    "h1",
    "h2",
    "h3",
    "br",
    "hr",
    "ul",
    "ol",
    "li",
    "blockquote",
    "strong",
    "em",
    "u",
    "s",
    "span",
    "pre",
    "code",
    "a",
}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "span": ["class"],
}
ALLOWED_PROTOCOLS = {"http", "https", "mailto"}


def clean_document_html(value: str) -> str:
    """Sanitize rich-text HTML before storing or rendering it."""
    return bleach.clean(
        value or "",
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def access_for(user, document: Document):
    """Return the user's document role, or None when they have no access."""
    if document.owner_id == user.id:
        return "owner"

    share = DocumentShare.objects.filter(
        document=document,
        user=user,
    ).first()
    return share.role if share else None


def require_access(user, document: Document, edit=False, owner=False):
    """Raise PermissionDenied unless the user has the requested access."""
    access = access_for(user, document)

    if (
        access is None
        or (owner and access != "owner")
        or (edit and access not in ("owner", "editor"))
    ):
        raise PermissionDenied

    return access
