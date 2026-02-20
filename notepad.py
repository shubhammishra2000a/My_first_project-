"""
Notepad App
Manage notes: add, view, and delete entries stored in notepad_data.json.
"""

import json
import os
from datetime import datetime

DATA_FILE = "notepad_data.json"


def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def add_note(notes):
    title = input("Note title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    print("Note content (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    content = "\n".join(lines).strip()
    note = {
        "id": max((n["id"] for n in notes), default=0) + 1,
        "title": title,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    notes.append(note)
    save_notes(notes)
    print(f"Note '{title}' saved.")


def view_notes(notes):
    if not notes:
        print("No notes found.")
        return
    print("\n--- Notes ---")
    for note in notes:
        print(f"[{note['id']}] {note['title']} ({note['created_at']})")
        if note["content"]:
            print(f"     {note['content']}")
    print()


def delete_note(notes):
    view_notes(notes)
    if not notes:
        return notes
    try:
        note_id = int(input("Enter note ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return notes
    updated = [n for n in notes if n["id"] != note_id]
    if len(updated) == len(notes):
        print("Note not found.")
    else:
        save_notes(updated)
        print("Note deleted.")
    return updated


def run():
    print("=== Notepad ===")
    notes = load_notes()
    while True:
        print("\n1. Add note\n2. View notes\n3. Delete note\n4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_note(notes)
        elif choice == "2":
            view_notes(notes)
        elif choice == "3":
            notes = delete_note(notes)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1–4.")


if __name__ == "__main__":
    run()
