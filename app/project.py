from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Session

from db import Base, get_db

from user import UserData

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

@router.post("/api/projects", tags=["projects"])
def create_project(project: Project, db: Session = Depends(get_db)):
    pdata = ProjectData(name=project.name, color=project.color, user_id=project.user_id)
    db.add(pdata)
    db.commit()
    db.refresh(pdata)
    return {"message": "Project created successfully"}

@router.get("/api/projects/{project_id}", tags=["projects"])
def get_project(project_id: int, db: Session = Depends(get_db)):
    pdata = fetch_project_by_id(db, project_id)
    if pdata is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return Project(name=pdata.name, color=pdata.color, user_id=pdata.user_id).dict()

@router.put("/api/projects/{project_id}", tags=["projects"])
def update_project(project_id: int, project: Project, db: Session = Depends(get_db)):
    db.query(ProjectData).filter(project_id==ProjectData.id).update(project.dict())
    db.commit()
    return {"message": "Project updated successfully"}

@router.delete("/api/projects/{project_id}", tags=["projects"])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db.query(ProjectData).filter(project_id==ProjectData.id).delete()
    db.commit()
    return {"message": "Project deleted successfully"}

def fetch_project_by_id(db: Session, project_id: int):
    return db.query(ProjectData).filter(ProjectData.id == project_id).first()
