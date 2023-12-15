import project, task, user, auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Main app module
app = FastAPI()

# List of allowed origins for CORS
origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:3000",
]

@app.get("/")
async def root():
    return {"message": "Root"}

# Tell fastapi to allow for CORS
# Done here because any other ordering seems to break CORS and I am scared to move anything
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

# Add routers from other files to avoid one monolithic file
app.include_router(auth.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(user.router)
