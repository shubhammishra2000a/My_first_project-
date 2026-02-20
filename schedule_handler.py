"""
Schedule Handler App
Manage scheduled tasks: add, view, and delete entries stored in schedule_data.json.
"""

import json
import os
from datetime import datetime

DATA_FILE = "schedule_data.json"


def load_schedules():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_schedules(schedules):
    with open(DATA_FILE, "w") as f:
        json.dump(schedules, f, indent=2)


def add_task(schedules):
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    date_str = input("Date and time (YYYY-MM-DD HH:MM): ").strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid date/time format. Use YYYY-MM-DD HH:MM.")
        return
    description = input("Description (optional): ").strip()
    task = {
        "id": max((t["id"] for t in schedules), default=0) + 1,
        "title": title,
        "datetime": date_str,
        "description": description,
    }
    schedules.append(task)
    save_schedules(schedules)
    print(f"Task '{title}' scheduled for {date_str}.")


def view_tasks(schedules):
    if not schedules:
        print("No scheduled tasks.")
        return
    print("\n--- Scheduled Tasks ---")
    for task in sorted(schedules, key=lambda t: t["datetime"]):
        print(f"[{task['id']}] {task['title']} | {task['datetime']}")
        if task["description"]:
            print(f"     {task['description']}")
    print()


def delete_task(schedules):
    view_tasks(schedules)
    if not schedules:
        return schedules
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return schedules
    updated = [t for t in schedules if t["id"] != task_id]
    if len(updated) == len(schedules):
        print("Task not found.")
    else:
        save_schedules(updated)
        print("Task deleted.")
    return updated


def run():
    print("=== Schedule Handler ===")
    schedules = load_schedules()
    while True:
        print("\n1. Add task\n2. View tasks\n3. Delete task\n4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_task(schedules)
        elif choice == "2":
            view_tasks(schedules)
        elif choice == "3":
            schedules = delete_task(schedules)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1–4.")


if __name__ == "__main__":
    run()
