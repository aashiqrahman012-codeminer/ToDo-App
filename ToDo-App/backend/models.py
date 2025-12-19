from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    done: bool

class Todo(BaseModel):
    id: int
    title: str
    done: bool