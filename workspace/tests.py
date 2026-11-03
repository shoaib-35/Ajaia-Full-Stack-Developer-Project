from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Document, DocumentShare


class DocumentWorkflowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner",
            password="StrongPass123!",
        )
        self.viewer = User.objects.create_user(
            username="viewer",
            password="StrongPass123!",
        )
        self.document = Document.objects.create(
            owner=self.owner,
            title="Test document",
            content="<p>Hello</p>",
        )

    def test_owner_can_open_and_document_persists(self):
        self.client.login(username="owner", password="StrongPass123!")

        response = self.client.get(
            reverse("document_detail", args=[self.document.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test document")

    def test_unshared_user_cannot_open_document(self):
        self.client.login(username="viewer", password="StrongPass123!")

        response = self.client.get(
            reverse("document_detail", args=[self.document.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_viewer_can_read_but_cannot_save(self):
        DocumentShare.objects.create(
            document=self.document,
            user=self.viewer,
            role=DocumentShare.VIEWER,
        )
        self.client.login(username="viewer", password="StrongPass123!")

        detail_response = self.client.get(
            reverse("document_detail", args=[self.document.pk])
        )
        save_response = self.client.post(
            reverse("document_save", args=[self.document.pk]),
            data='{"content":"<p>Changed</p>"}',
            content_type="application/json",
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(save_response.status_code, 403)

        self.document.refresh_from_db()
        self.assertEqual(self.document.content, "<p>Hello</p>")

    def test_editor_can_save_sanitized_content(self):
        DocumentShare.objects.create(
            document=self.document,
            user=self.viewer,
            role=DocumentShare.EDITOR,
        )
        self.client.login(username="viewer", password="StrongPass123!")

        response = self.client.post(
            reverse("document_save", args=[self.document.pk]),
            data=(
                '{"content":"<p>Safe</p>'
                '<script>alert(1)</script>"}'
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.document.refresh_from_db()
        self.assertNotIn("<script>", self.document.content)


class SignUpTests(TestCase):
    def test_signup_page_is_available_and_creates_authenticated_user(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("signup"),
            {
                "username": "newmember",
                "first_name": "New",
                "last_name": "Member",
                "email": "newmember@example.com",
                "password1": "StrongPass!2026",
                "password2": "StrongPass!2026",
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(
            User.objects.filter(username="newmember").exists()
        )
        self.assertIn("_auth_user_id", self.client.session)
