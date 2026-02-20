"""
Tests for schedule_handler and notepad modules.
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import notepad
import schedule_handler


class TestScheduleHandler(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        schedule_handler.DATA_FILE = self.tmp.name
        # Start with an empty file
        with open(self.tmp.name, "w") as f:
            json.dump([], f)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_load_empty(self):
        data = schedule_handler.load_schedules()
        self.assertEqual(data, [])

    def test_save_and_load(self):
        tasks = [{"id": 1, "title": "Meeting", "datetime": "2026-03-01 09:00", "description": ""}]
        schedule_handler.save_schedules(tasks)
        loaded = schedule_handler.load_schedules()
        self.assertEqual(loaded, tasks)

    def test_add_task(self):
        schedules = []
        with patch("builtins.input", side_effect=["Stand-up", "2026-03-01 09:00", ""]):
            schedule_handler.add_task(schedules)
        loaded = schedule_handler.load_schedules()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "Stand-up")
        self.assertEqual(loaded[0]["datetime"], "2026-03-01 09:00")

    def test_add_task_invalid_date(self):
        schedules = []
        with patch("builtins.input", side_effect=["Bad Task", "not-a-date", ""]):
            schedule_handler.add_task(schedules)
        # Nothing should be saved
        loaded = schedule_handler.load_schedules()
        self.assertEqual(loaded, [])

    def test_add_task_empty_title(self):
        schedules = []
        with patch("builtins.input", side_effect=[""]):
            schedule_handler.add_task(schedules)
        loaded = schedule_handler.load_schedules()
        self.assertEqual(loaded, [])

    def test_delete_task(self):
        schedules = [
            {"id": 1, "title": "Task A", "datetime": "2026-03-01 10:00", "description": ""},
            {"id": 2, "title": "Task B", "datetime": "2026-03-02 10:00", "description": ""},
        ]
        schedule_handler.save_schedules(schedules)
        with patch("builtins.input", side_effect=["1"]):
            result = schedule_handler.delete_task(schedules)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 2)

    def test_delete_task_not_found(self):
        schedules = [
            {"id": 1, "title": "Task A", "datetime": "2026-03-01 10:00", "description": ""}
        ]
        schedule_handler.save_schedules(schedules)
        with patch("builtins.input", side_effect=["99"]):
            result = schedule_handler.delete_task(schedules)
        # Task not found — original list returned unchanged
        self.assertEqual(result, schedules)

    def test_view_tasks_empty(self):
        with patch("builtins.print") as mock_print:
            schedule_handler.view_tasks([])
            mock_print.assert_any_call("No scheduled tasks.")


class TestNotepad(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.tmp.close()
        notepad.DATA_FILE = self.tmp.name
        with open(self.tmp.name, "w") as f:
            json.dump([], f)

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_load_empty(self):
        data = notepad.load_notes()
        self.assertEqual(data, [])

    def test_save_and_load(self):
        notes = [{"id": 1, "title": "Hello", "content": "World", "created_at": "2026-02-20 10:00"}]
        notepad.save_notes(notes)
        loaded = notepad.load_notes()
        self.assertEqual(loaded, notes)

    def test_add_note(self):
        notes = []
        # Title, one line of content, then two empty lines to finish
        with patch("builtins.input", side_effect=["My Note", "Some content", "", ""]):
            notepad.add_note(notes)
        loaded = notepad.load_notes()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "My Note")
        self.assertIn("Some content", loaded[0]["content"])

    def test_add_note_empty_title(self):
        notes = []
        with patch("builtins.input", side_effect=[""]):
            notepad.add_note(notes)
        loaded = notepad.load_notes()
        self.assertEqual(loaded, [])

    def test_delete_note(self):
        notes = [
            {"id": 1, "title": "Note A", "content": "aaa", "created_at": "2026-02-20 10:00"},
            {"id": 2, "title": "Note B", "content": "bbb", "created_at": "2026-02-20 11:00"},
        ]
        notepad.save_notes(notes)
        with patch("builtins.input", side_effect=["1"]):
            result = notepad.delete_note(notes)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 2)

    def test_delete_note_not_found(self):
        notes = [
            {"id": 1, "title": "Note A", "content": "aaa", "created_at": "2026-02-20 10:00"}
        ]
        notepad.save_notes(notes)
        with patch("builtins.input", side_effect=["99"]):
            result = notepad.delete_note(notes)
        self.assertEqual(result, notes)

    def test_view_notes_empty(self):
        with patch("builtins.print") as mock_print:
            notepad.view_notes([])
            mock_print.assert_any_call("No notes found.")


if __name__ == "__main__":
    unittest.main()
