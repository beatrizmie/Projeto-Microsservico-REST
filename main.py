from fastapi import FastAPI, Query
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
import uuid

class Task(BaseModel):
    name: Optional[str]
    description: str = Field(..., description="Breve descrição da tarefa", min_length=3, max_length=50)
    is_done: bool = False

task_list = {}

app = FastAPI()

#CREATE NEW TASK
@app.post("/tasks/{task_id}")
async def create_task(task: Task):
    task_id = uuid.uuid4()
    task_dict = task.dict()
    task_list[task_id] = task_dict
    return {task_id: task_dict}


#READ ALL TASKS
@app.get("/tasks/")
async def list_tasks():
    return task_list


#READ ALL DONE TASKS OR ALL NOT DONE TASKS
@app.get("/tasks/list/{is_done}")
async def list_tasks_done(is_done: bool):
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
@app.put("/tasks/{task_id}/name")
async def update_task_name(task_id: UUID, task_name: str):
    if task_id in task_list:
        task_list[task_id].update({"name": task_name})
        return {task_id: task_list[task_id]}
    return "The task {task_id} doesn't exist!"


#UPDATE TASK DESCRIPTION
@app.put("/tasks/{task_id}/description")
async def update_task_description(task_id: UUID, task_description: str):
    if task_description.len() < 3:
        return "Task description must have at least 3 characters!"
    if task_id in task_list:
        task_list[task_id].update({"description": task_description})
        return {task_id: task_list[task_id]}
    return "The task {task_id} doesn't exist!"


#UPDATE TASK IS_DONE
@app.put("/tasks/{task_id}/is_done")
async def update_task_is_done(task_id: UUID):
    if task_id in task_list:
        if task_list[task_id]["is_done"] == True:
            task_list[task_id].update({"is_done": False})
        else:
            task_list[task_id].update({"is_done": True})
        return {task_id: task_list[task_id]}
    return "The task {task_id} doesn't exist!"


#DELETE TASK
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: UUID):
    if task_id in task_list:
        del task_list[task_id]
        return task_list
    return "The task {task_id} doesn't exist!"
