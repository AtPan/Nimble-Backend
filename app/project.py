from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, select, update, delete
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from user import User

from db import Base, get_db

from user import fetch_user_by_email

router = APIRouter()

class ProjectData(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True)
    color = Column(String)
    user_id = Column(ForeignKey("users.id"))
    

class Project(BaseModel):
    name: str
    color: str
    user_id: int
    class Config:
        orm_mode = True

@router.get("/api/allprojects", tags=["projects"])
def get_all_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = fetch_user_by_email(db, current_user.email).id
    projects = db.query(ProjectData).filter_by(user_id=user_id).all()
    print(f"Projects: {projects}")
    return projects

@router.post("/api/projects", tags=["projects"])
def create_project(project: Project, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    userData = fetch_user_by_email(db, current_user.email)
    pdata = ProjectData(name=project.name, color=project.color, user_id=userData.id)
    db.add(pdata)
    db.commit()
    db.refresh(pdata)
    return {"message": "Project created successfully"}

@router.get("/api/projects/{project_id}", tags=["projects"])
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pdata = fetch_project_by_id(db, project_id)
    if pdata is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return Project(name=pdata.name, color=pdata.color, user_id=pdata.user_id).dict()

@router.put("/api/projects/{project_id}", tags=["projects"])
def update_project(project_id: int, project: Project, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.execute(update(ProjectData).where(ProjectData.id==project_id).values({
        ProjectData.name: project.name,
        ProjectData.color: project.color
    }))
    db.commit()
    return {"message": "Project updated successfully"}

@router.delete("/api/projects/{project_id}", tags=["projects"])
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.execute(delete(ProjectData).where(ProjectData.id==project_id))
    db.commit()
    return {"message": "Project deleted successfully"}

def fetch_project_by_id(db: Session, project_id: int):
    return db.execute(select(ProjectData).filter_by(ProjectData.id==project_id)).first()
