from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

app = FastAPI(title="Task Manager API")

class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(BaseModel):
    title: str = Field(..., example="Finish writing blog post")
    description: Optional[str] = Field(None, example="For the company site")
    status: StatusEnum = Field(..., example="pending")
    priority: PriorityEnum = Field(..., example="high")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[StatusEnum]
    priority: Optional[PriorityEnum]

class Task(TaskBase):
    id: int

tasks: List[Task] = []
id_counter: int = 1


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    global id_counter
    new_task = Task(id=id_counter, **task.dict())
    tasks.append(new_task)
    id_counter += 1
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated: TaskUpdate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_data = updated.dict(exclude_unset=True)
            updated_task = task.copy(update=updated_data)
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return
    raise HTTPException(status_code=404, detail="Task not found")
