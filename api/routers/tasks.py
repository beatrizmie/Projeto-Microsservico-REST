from fastapi import Depends, FastAPI, HTTPException, Query, status, APIRouter
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
import uuid

from api.models import Task
from api.database import get_db, DBSession

router = APIRouter()


#CREATE NEW TASK
@router.post("/{task_id}", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task, db: DBSession = Depends(get_db)):
    task_id = uuid.uuid4()
    task_dict = task.dict()
    task_dict.update({"is_done": False})
    db.task_list[task_id] = task_dict
    return task_dict


#READ ALL TASKS
@router.get("/")
async def list_all_tasks(db: DBSession = Depends(get_db)):
    return db.return_tasks_list()


#READ ALL DONE TASKS OR ALL NOT DONE TASKS
@router.get("/list/{is_done}")
async def list_tasks_done_or_not_done(is_done: bool, db: DBSession = Depends(get_db)):
    
    done_tasks, not_done_tasks = db.check_done_or_not_done()

    if is_done:
        return done_tasks
    else:
        return not_done_tasks


#UPDATE TASK NAME
@router.put("/{task_id}/name")
async def update_task_name(task_id: UUID, task_name: str, db: DBSession = Depends(get_db)):
    return db.update_task_string(task_id, task_name, "name")


#UPDATE TASK DESCRIPTION
@router.put("/{task_id}/description")
async def update_task_description(task_id: UUID, task_description: str, db: DBSession = Depends(get_db)):
    if len(task_description) < 3:
        return "Task description must have at least 3 characters!"
    return db.update_task_string(task_id, task_description, "description")


#UPDATE TASK IS_DONE
@router.put("/{task_id}/is_done")
async def update_task_is_done(task_id: UUID, db: DBSession = Depends(get_db)):
    return db.update_task_is_done(task_id)


#DELETE TASK
@router.delete("/{task_id}")
async def delete_task(task_id: UUID, db: DBSession = Depends(get_db)):
    db.delete_task(task_id)