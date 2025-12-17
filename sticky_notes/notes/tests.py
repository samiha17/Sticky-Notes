from django.test import TestCase
from django.urls import reverse
from .models import Note
from .forms import NoteForm


# Create your tests here.
class StickyNotesTestCase(TestCase):
    def setUp(self):
        # Sample Note
        self.note = Note.objects.create(title="Sample Note", content="Sample content")

    # Model Tests
    def test_create_note(self):
        note = Note.objects.create(title="Test Note", content="This is a test note")
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "This is a test note")
        self.assertIsNotNone(note.created_at)

    # Form Tests
    def test_valid_note_form(self):
        data = {"title": "Valid Title", "content": "Valid Content"}
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_note_form(self):
        data = {"title": "", "content": ""}
        form = NoteForm(data=data)
        self.assertFalse(form.is_valid())

    # View Tests
    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)

    def test_note_create_view(self):
        response = self.client.post(
            reverse("note_create"), {"title": "New Note", "content": "New Content"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_note_update_view(self):
        response = self.client.post(
            reverse("note_update", args=[self.note.id]),
            {
                "title": "Updated Note",
                "content": "Updated Content",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Note")

    def test_note_delete_view(self):
        response = self.client.post(reverse("note_delete", args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
