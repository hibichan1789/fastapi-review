from fastapi import FastAPI
from tasks.tasks_router import tasks_router

app = FastAPI()
app.include_router(tasks_router)