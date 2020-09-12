from fastapi import FastAPI, Query, status
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
import uuid

tags_metadata = [
    {
        "name": "task",
        "description": "Operations with task list",
    }
]

app = FastAPI(openapi_tags=tags_metadata)


class Task(BaseModel):
    name: str = Field(None, title="Task name", description="optional")
    description: str = Field(..., description="Brief task description", min_length=3, max_length=50)

task_list = {}


#CREATE NEW TASK
@app.post("/tasks/{task_id}", status_code=status.HTTP_201_CREATED, tags=["task"])
async def create_task(task: Task):
    task_id = uuid.uuid4()
    task_dict = task.dict()
    task_dict.update({"is_done": False})
    task_list[task_id] = task_dict
    return {task_id: task_dict}


#READ ALL TASKS
@app.get("/tasks/", tags=["task"])
async def list_all_tasks():
    return task_list


#READ ALL DONE TASKS OR ALL NOT DONE TASKS
@app.get("/tasks/list/{is_done}", tags=["task"])
async def list_tasks_done_or_not_done(is_done: bool):
    result1 = {}
    result2 = {}

    for task_id in task_list:
        if task_list[task_id]["is_done"] == 1:
            result1[task_id] = task_list[task_id]
        else:
            result2[task_id] = task_list[task_id]
    
    if is_done:
        return result1
    else:
        return result2


#UPDATE TASK NAME
@app.put("/tasks/{task_id}/name", tags=["task"])
async def update_task_name(task_id: UUID, task_name: str):
    if task_id in task_list:
        task_list[task_id].update({"name": task_name})
        return {task_id: task_list[task_id]}
    return "The task {task_id} doesn't exist!"


#UPDATE TASK DESCRIPTION
@app.put("/tasks/{task_id}/description", tags=["task"])
async def update_task_description(task_id: UUID, task_description: str):
    if task_description.len() < 3:
        return "Task description must have at least 3 characters!"
    if task_id in task_list:
        task_list[task_id].update({"description": task_description})
        return {task_id: task_list[task_id]}
    return "The task {task_id} doesn't exist!"


#UPDATE TASK IS_DONE
@app.put("/tasks/{task_id}/is_done", tags=["task"])
async def update_task_is_done(task_id: UUID):
    if task_id in task_list:
        if task_list[task_id]["is_done"] == True:
            task_list[task_id].update({"is_done": False})
        else:
            task_list[task_id].update({"is_done": True})
        return {task_id: task_list[task_id]}
    return "The task {task_id} doesn't exist!"


#DELETE TASK
@app.delete("/tasks/{task_id}", tags=["task"])
async def delete_task(task_id: UUID):
    if task_id in task_list:
        del task_list[task_id]
        return task_list
    return "The task {task_id} doesn't exist!"


#CUSTOMIZE DOCUMENTATION
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="APS 1 - Megadados",
        version="2.5.0",
        description="Project: task list using Fast API.\nAuthors: Beatriz Mie and Samuel Porto",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://upload.wikimedia.org/wikipedia/pt/3/39/Logo_Insper.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi