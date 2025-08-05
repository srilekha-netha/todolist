import json
import os

TASK_FILE = "data/tasks.json"
TRASH_FILE = "data/deleted_tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def load_deleted_tasks():
    if os.path.exists(TRASH_FILE):
        with open(TRASH_FILE, "r") as f:
            return json.load(f)
    return []

def save_deleted_tasks(deleted):
    with open(TRASH_FILE, "w") as f:
        json.dump(deleted, f, indent=4)

def add_task(tasks, text):
    tasks.append({"task": text, "done": False})
    return tasks

def toggle_task(tasks, index):
    tasks[index]["done"] = not tasks[index]["done"]
    return tasks

def delete_task(tasks, index):
    deleted = load_deleted_tasks()
    deleted.append(tasks[index])
    save_deleted_tasks(deleted)
    del tasks[index]
    return tasks

def update_task(tasks, index, new_text):
    tasks[index]["task"] = new_text
    return tasks

def filter_tasks(tasks, status):
    if status == "Completed":
        return [t for t in tasks if t["done"]]
    elif status == "Pending":
        return [t for t in tasks if not t["done"]]
    return tasks
