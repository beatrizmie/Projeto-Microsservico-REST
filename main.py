from fastapi import Depends, FastAPI, HTTPException, Query, status
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

app = FastAPI(
    title='Tasks List',
    description='Tasks list project for the **Megadados** course',
    openapi_tags=tags_metadata
    )


class Task(BaseModel):
    name: str = Field(None, title="Task name", description="optional")
    description: str = Field(..., description="Brief task description", min_length=3, max_length=50)

test_uuid =[
    UUID('d5c1c91b-3cf3-4694-861c-1f7935f12ab2'), 
    UUID('d5c1c91b-3cf3-4694-861c-1f7935f12ab3'),
    UUID('d5c1c91b-3cf3-4694-861c-1f7935f12ab4'),
    UUID('d5c1c91b-3cf3-4694-861c-1f7935f12ab5')
] 

class DBSession:
    task_list = {
        test_uuid[0]: {
            "name": "hello",
            "description": "hello everyone",
            "is_done": False
        },
        test_uuid[1]: {
            "name": "bia",
            "description": "heyy bia",
            "is_done": False
        },
        test_uuid[2]:  {
            "name": "samu",
            "description": "heyy samu",
            "is_done": False
        },
        test_uuid[3]:  {
            "name": "samu",
            "description": "heyy samu",
            "is_done": True
        },
    }

    def __init__(self):
        self.task_list = DBSession.task_list

    def return_tasks_list(self):
        return self.task_list

    def task_in_task_list(self, task_id: UUID):
        if task_id in self.task_list:
            return True
        else:
            return False

    def check_done_or_not_done(self):
        done_tasks = {}
        not_done_tasks = {}

        for task in self.task_list:
            if self.task_list[task]["is_done"] == True:
                done_tasks[task] = self.task_list[task]
            else:
                not_done_tasks[task] = self.task_list[task]

        return done_tasks, not_done_tasks

    def update_task(self, task_id: UUID, dictionary: dict()):
        if self.task_in_task_list(task_id):
            self.task_list[task_id].update(dictionary)
            self.return_tasks_list()
        else:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            )


def get_db():
    return DBSession()


#CREATE NEW TASK
@app.post("/tasks/{task_id}", status_code=status.HTTP_201_CREATED, tags=["task"])
async def create_task(task: Task, db: DBSession = Depends(get_db)):
    task_id = uuid.uuid4()
    task_dict = task.dict()
    task_dict.update({"is_done": False})
    db.task_list[task_id] = task_dict
    return task_dict


#READ ALL TASKS
@app.get("/tasks/", tags=["task"])
async def list_all_tasks(db: DBSession = Depends(get_db)):
    return db.return_tasks_list


#READ ALL DONE TASKS OR ALL NOT DONE TASKS
@app.get("/tasks/list/{is_done}", tags=["task"])
async def list_tasks_done_or_not_done(is_done: bool, db: DBSession = Depends(get_db)):
    
    done_tasks, not_done_tasks = db.check_done_or_not_done()

    if is_done:
        return done_tasks
    else:
        return not_done_tasks


#UPDATE TASK NAME
@app.put("/tasks/{task_id}/name", tags=["task"])
async def update_task_name(task_id: UUID, task_name: str, db: DBSession = Depends(get_db)):
    db.update_task(task_id, {"name": task_name})


#UPDATE TASK DESCRIPTION
@app.put("/tasks/{task_id}/description", tags=["task"])
async def update_task_description(task_id: UUID, task_description: str, db: DBSession = Depends(get_db)):
    if len(task_description) < 3:
        return "Task description must have at least 3 characters!"
    db.update_task(task_id, {"description": task_description})


#UPDATE TASK IS_DONE
@app.put("/tasks/{task_id}/is_done", tags=["task"])
async def update_task_is_done(task_id: UUID, db: DBSession = Depends(get_db)):
    if task_id in db.task_list:
        if db.task_list[task_id]["is_done"] == True:
            db.task_list[task_id].update({"is_done": False})
        else:
            db.task_list[task_id].update({"is_done": True})
        return db.task_list[task_id]
    else:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )


#DELETE TASK
@app.delete("/tasks/{task_id}", tags=["task"])
async def delete_task(task_id: UUID, db: DBSession = Depends(get_db)):
    if task_id in db.task_list:
        del db.task_list[task_id]
    else:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )


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