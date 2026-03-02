from fastapi import APIRouter, HTTPException, Path
from typing import Annotated
from .tasks_models import Task, TaskRequest, TaskResponse, Status
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

task_mock:list[Task] = []

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.post("", status_code=201, response_model=TaskResponse)
def create_task(task_request:TaskRequest):
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    diff = now - task_request.deadline
    if diff.total_seconds() > 0:
        raise HTTPException(status_code=400, detail="deadline is invalid")
    priority_score=calculate_priority_score(importance=task_request.importance, urgency=task_request.urgency)
    task = Task(**task_request.model_dump(), priority_score=priority_score)
    task_mock.append(task)
    return task

@tasks_router.get("", response_model=list[TaskResponse])
def get_all_tasks():
    return task_mock

@tasks_router.patch("/{task_id}/status")
def patch_task_status(task_id:Annotated[str, Path(...)], status:Status):
    print(task_id)
    target_task = get_target_task(task_id)
    if target_task == None:
        raise HTTPException(status_code=404, detail="task not found")
    target_task.status = status
    return target_task

@tasks_router.get("/analytics")
def get_analytics_data():
    average_priority_score, result = generate_analytics(task_mock)
    return {"average_priority_score": average_priority_score, **result}

# 仮のutil
def calculate_priority_score(importance:int, urgency:int)->float:
    return (importance * 0.7) + (urgency * 0.3)
def generate_analytics(tasks:list[Task]):
    result = {Status.todo:0.0, Status.in_progress:0.0, Status.done:0.0}
    sum_priority_scores = 0
    for task in tasks:
        sum_priority_scores += task.priority_score
        result[task.status] += task.priority_score
    average_priority_score = sum_priority_scores/len(tasks) if len(tasks) != 0 else sum_priority_scores
    return average_priority_score, result
def get_target_task(target_id:str)->Task|None:
    target_uuid = UUID(target_id)
    for task in task_mock:
        if task.id == target_uuid:
            return task
    return None
