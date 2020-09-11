from fastapi import FastAPI, Query
from pydantic import Field, BaseModel
from uuid import UUID

class Task(BaseModel):
    name: str
    description: str = Field(..., description="Breve descrição da tarefa", min_length=3, max_length=50)
    is_done: bool = False

task_list = {}

app = FastAPI()

#CREATE NEW TASK
@app.post("/tasks/")
async def create_task(task: Task):
    task_dict = task.dict()
    task_list[task.name] = task_dict
    return task_dict


#READ TASK
@app.get("/tasks/")
async def list_tasks():
    return task_list

@app.get("/tasks/list/{is_done}")
async def list_is_done_tasks(is_done: bool):
    result1 = {}
    result2 = {}

    for task_name in task_list:
        if task_list[task_name]["is_done"] == 1:
            result1[task_name] = task_list[task_name]
        else:
            result2[task_name] = task_list[task_name]
    
    if is_done:
        return result1
    else:
        return result2

#UPDATE TASK DESCRIPTION
@app.put("/tasks/{task_name}/description")
async def update_task_description(task_name: str, task_description: str):
    if task_name in task_list:
        task_list[task_name].update({"description": task_description})
    return task_list


#UPDATE TASK IS_DONE
@app.put("/tasks/{task_name}/is_done")
async def update_task_is_done(task_name: str):
    if task_name in task_list:
        if task_list[task_name]["is_done"] == True:
            task_list[task_name].update({"is_done": False})
        else:
            task_list[task_name].update({"is_done": True})
    return task_list


#DELETE TASK
@app.delete("/tasks/{task_name}")
async def delete_task(task_name: str):
    if task_name in task_list:
        del task_list[task_name]
    return task_list
