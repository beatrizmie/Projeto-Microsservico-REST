from fastapi import Depends, FastAPI, HTTPException, Query, status
from uuid import UUID


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

    def update_task_string(self, task_id: UUID, task: str, key: str):
        if self.task_in_task_list(task_id):
            self.task_list[task_id].update({key: task})
            return self.task_list[task_id]
        else:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            )

    def update_task_is_done(self, task_id: UUID):
        if self.task_in_task_list(task_id):
            if self.task_list[task_id]["is_done"] == True:
                self.task_list[task_id].update({"is_done": False})
            else:
                self.task_list[task_id].update({"is_done": True})
            return self.task_list[task_id]
        else:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            )

    def delete_task(self, task_id: UUID):
        if self.task_in_task_list(task_id):
            del self.task_list[task_id]
        else:
            raise HTTPException(
                status_code=404,
                detail='Task not found',
            )


def get_db():
    return DBSession()