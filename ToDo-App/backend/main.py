from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ← IMPORTANT!
from typing import List
import pandas as pd
from datetime import datetime, timedelta
from models import Todo, TodoCreate, TodoUpdate
from storage import add_todo, load_todos, update_todo, delete_todo, load_raw_todos

app = FastAPI(title="King's To-Do API")

# ADD CORS MIDDLEWARE (allows frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/todos")
def get_todos():
    return load_todos()

@app.post("/todos")
def create_todo(todo: TodoCreate):
    return add_todo(todo.title)

@app.put("/todos/{todo_id}")
def mark_todo_done(todo_id: int, update: TodoUpdate):
    try:
        return update_todo(todo_id, update.done)
    except ValueError:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def remove_todo(todo_id: int):
    delete_todo(todo_id)
    return {"message": "Deleted"}

@app.get("/analytics")
def get_analytics():
    raw_tasks = load_raw_todos()
    if not raw_tasks:
        return {"message": "No tasks yet!"}

    df = pd.DataFrame(raw_tasks)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["completed_at"] = pd.to_datetime(df["completed_at"], errors='coerce')
    
    total = len(df)
    completed = df[df["status"] == "done"]
    completed_count = len(completed)
    completion_rate = round((completed_count / total) * 100, 1) if total > 0 else 0
    
    week_ago = datetime.now() - timedelta(days=7)
    completed_this_week = completed[completed["completed_at"] >= week_ago]
    weekly_count = len(completed_this_week)
    
    df["created_day"] = df["created_at"].dt.day_name()
    most_active_day = df["created_day"].mode()
    most_active = most_active_day[0] if not most_active_day.empty else "N/A"
    
    return {
        "total_tasks": total,
        "completed_tasks": completed_count,
        "completion_rate_percent": completion_rate,
        "completed_this_week": weekly_count,
        "most_active_day": most_active
    }