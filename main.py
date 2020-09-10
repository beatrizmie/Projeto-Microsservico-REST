from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from uuid import UUID

class Tarefa(BaseModel):
    name: str
    description: str = Field(..., description="Breve descrição da tarefa", min_length=3, max_length=50)
    is_done: bool

lista_tarefas = {}

app = FastAPI()

#CREATE NEW TAREFA
@app.post("/tarefa")
async def create_tarefa(tarefa: Tarefa):
    tarefa_dict = tarefa.dict()
    lista_tarefas[tarefa.name] = tarefa_dict
    return tarefa_dict

#READ TAREFA
@app.get("/tarefas")
async def get_tarefas():
    return lista_tarefas

#UPDATE TAREFA
@app.put("/tarefa/{id_tarefa}")
async def update_tarefa(id_tarefa: int, tarefa: Tarefa):
    return {"id_tarefa": id_tarefa, **tarefa.dict()}

#DELETE TAREFA
@app.delete("/tarefa/{id_tarefa}")
async def delete_tarefa(id_tarefa: int, tarefa: Tarefa):
    for i in lista_tarefas:
        if tarefa == i:
            lista_tarefas.remove(i)
