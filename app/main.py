from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import project, task, user, auth3

app = FastAPI()

origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://fastapi-app:8000",
]

@app.get("/")
async def greet():
    return {"message": "Hello World"}

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(auth3.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(user.router)
