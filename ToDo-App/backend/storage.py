import os
from datetime import datetime
from typing import List

TODO_FILE = "todos.txt"

def _now_str():
    return datetime.now().isoformat()

def _load_raw_todos():
    if not os.path.exists(TODO_FILE):
        return []
    raw_tasks = []
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("|", 4)
                if len(parts) == 5:
                    raw_tasks.append({
                        "id": int(parts[0]),
                        "status": parts[1],
                        "title": parts[2],
                        "created_at": parts[3],
                        "completed_at": None if parts[4] == "None" else parts[4]
                    })
    return raw_tasks

def _save_raw_todos(raw_tasks):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        for task in raw_tasks:
            completed = task["completed_at"] or "None"
            f.write(f'{task["id"]}|{task["status"]}|{task["title"]}|{task["created_at"]}|{completed}\n')

def add_todo(title: str):
    from models import Todo
    raw_tasks = _load_raw_todos()
    new_id = max([t["id"] for t in raw_tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "status": "pending",
        "title": title,
        "created_at": _now_str(),
        "completed_at": None
    }
    raw_tasks.append(new_task)
    _save_raw_todos(raw_tasks)
    return Todo(id=new_id, title=title, done=False)

def update_todo(todo_id: int, done: bool):
    from models import Todo
    raw_tasks = _load_raw_todos()
    for task in raw_tasks:
        if task["id"] == todo_id:
            task["status"] = "done" if done else "pending"
            if done and not task["completed_at"]:
                task["completed_at"] = _now_str()
            elif not done:
                task["completed_at"] = None
            _save_raw_todos(raw_tasks)
            return Todo(id=todo_id, title=task["title"], done=done)
    raise ValueError("Todo not found")

def delete_todo(todo_id: int):
    raw_tasks = _load_raw_todos()
    raw_tasks = [t for t in raw_tasks if t["id"] != todo_id]
    _save_raw_todos(raw_tasks)

def load_todos():
    from models import Todo
    raw_tasks = _load_raw_todos()
    return [Todo(id=t["id"], title=t["title"], done=t["status"]=="done") for t in raw_tasks]

load_raw_todos = _load_raw_todos