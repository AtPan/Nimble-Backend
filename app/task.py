from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, Column, Integer, String, select, delete
from sqlalchemy.orm import Session, column_property
from oauth2 import get_current_user
from user import User, fetch_user_by_email
from db import Base, get_db

router = APIRouter()

# ORM representation of Task. See project.py for more information
class TaskData(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    description = Column(String)
    due_date = Column(String)
    user_id = Column(ForeignKey("users.id"))
    project_id = Column(ForeignKey("projects.id"))
    is_checked = column_property(Column(Integer, default=False, name="completed"))

# Task representation for communications with the front end
class Task(BaseModel):
    name: str
    description: str
    due_date: str
    user_id: int
    project_id: int
    completed: int = Field(alias="is_checked")
    class Config:
        orm_mode = True

# Creates a task. Information must be sent as form data.
@router.post("/api/tasks", tags=["tasks"])
def create_task(task: Task, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = fetch_user_by_email(db, current_user.email).id
    tdata = TaskData(name=task.name,
                     description=task.description,
                     due_date=task.due_date,
                     user_id=user_id,
                     project_id=task.project_id)

    db.add(tdata)
    db.commit()
    db.refresh(tdata)
    return {"message": "Task created successfully"}

# Retreives a task by id. If the id does not correlate to a task, a 404 is returned.
@router.get("/api/tasks/{task_id}", tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tdata = fetch_task_by_id(db, task_id)
    if tdata is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(name=tdata.name, description=tdata.description, due_date=tdata.due_date, user_id=tdata.user_id, project_id=tdata.project_id, completed=tdata.is_checked).dict()

# Retreives all tasks of a given user.
@router.get("/api/alltasks", tags=["tasks"])
def get_all_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = fetch_user_by_email(db, current_user.email).id
    all_tasks = db.query(TaskData).filter_by(user_id=user_id).all()
    return all_tasks

# Modifies a given task by its id.
@router.put("/api/tasks/{task_id}", tags=["tasks"])
def update_task(task_id: int, task: Task, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tdata = fetch_task_by_id(db, task_id)
    if tdata != None:
        db.query(TaskData).filter(TaskData.id==task_id).update({
            TaskData.name: task.name,
            TaskData.description: task.description,
            TaskData.due_date: task.due_date,
            TaskData.is_checked: task.completed,
        })
        db.commit()
        return {"message": "Task updated successfully"}
    return {"message": "No task exists"}

# Removes a task by its id.
@router.delete("/api/tasks/{task_id}", tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.execute(delete(TaskData).where(TaskData.id==task_id))
    db.commit()
    return {"message": "Task deleted successfully"}

def fetch_task_by_id(db: Session, task_id: int):
    row = db.execute(select(TaskData).filter_by(id=task_id)).first()
    if row != None:
        row = row[0]
    return row
