from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
import uuid

from .models import Task
from .database import get_db, DBSession
from api.routers import tasks


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


app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["task"]
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