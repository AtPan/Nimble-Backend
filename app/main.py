from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import project, task, user, auth3

app = FastAPI()

origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:5173"
]
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
)

app.include_router(auth3.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(user.router)


#engine=create_engine(SQL_DB)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base = declerative_base()

@app.get("/")
async def greet():
    return {"message": "Hello World"}

