from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session
from oauth2 import get_current_user
from user import User

from db import Base, get_db

router = APIRouter()

class TaskData(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    description = Column(String)
    due_date = Column(String)
    user_id = Column(ForeignKey("users.id"))
    project_id = Column(ForeignKey("projects.id"))

class Task(BaseModel):
    name: str
    description: str
    due_date: str
    user_id: int
    project_id: int
    class Config:
        orm_mode = True

@router.post("/api/tasks", tags=["tasks"])
def create_task(task: Task, db: Session = Depends(get_db)):
    tdata = TaskData(name=task.name, description=task.description, due_date=task.due_date, user_id=task.user_id, project_id=task.project_id)
#    tdata = TaskData()
#    tdata.name = Column(task.name)
#    tdata.description = Column(task.description)
#    tdata.due_date = Column(task.due_date)
#    tdata.user_id = Column(task.user_id)
#    tdata.project_id = Column(task.project_id)

    db.add(tdata)
    db.commit()
    db.refresh(tdata)
    return {"message": "Task created successfully"}

@router.get("/api/tasks/{task_id}", tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    tdata = fetch_task_by_id(db, task_id)
    if tdata is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(name=tdata.name, description=tdata.description, due_date=tdata.due_date, user_id=tdata.user_id, project_id=tdata.project_id).dict()

@router.get("/api/alltasks", tags=["tasks"])
def get_all_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(TaskData).all()

@router.put("/api/tasks/{task_id}", tags=["tasks"])
def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    tdata = fetch_task_by_id(db, task_id)
    db.query(TaskData).filter(task_id==TaskData.id).update(task.dict())
    db.commit()
    return {"message": "Task updated successfully"}

@router.delete("/api/tasks/{task_id}", tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db.query(TaskData).filter(task_id==TaskData.id).delete()
    db.commit()
    return {"message": "Task deleted successfully"}

def fetch_task_by_id(db: Session, task_id: int):
    return db.query(TaskData).filter(TaskData.id == task_id).first()
