# My_first_project-

A beginner Python project containing two simple CLI apps:

## Apps

### 1. Schedule Handler
Manage time-based tasks. Tasks are saved locally in `schedule_data.json`.

**Features**
- Add a task with a title, date/time (`YYYY-MM-DD HH:MM`), and optional description
- View all tasks sorted by date
- Delete a task by ID

**Run**
```bash
python schedule_handler.py
```

---

### 2. Notepad
Manage freeform text notes. Notes are saved locally in `notepad_data.json`.

**Features**
- Add a note with a title and multi-line content
- View all notes with their creation timestamp
- Delete a note by ID

**Run**
```bash
python notepad.py
```

---

### Combined launcher
A single entry point that lets you pick which app to open.

```bash
python main.py
```

---

## Tests

```bash
python -m unittest test_apps -v
```
