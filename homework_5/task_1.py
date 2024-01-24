"""
Необходимо создать API для управления списком задач. Каждая задача должна
содержать заголовок и описание. Для каждой задачи должна быть возможность
указать статус (выполнена/не выполнена).
API должен содержать следующие конечные точки:
○ GET /tasks - возвращает список всех задач.
○ GET /tasks/{id} - возвращает задачу с указанным идентификатором.
○ POST /tasks - добавляет новую задачу.
○ PUT /tasks/{id} - обновляет задачу с указанным идентификатором.
○ DELETE /tasks/{id} - удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и
ответа. Для этого использовать библиотеку Pydantic.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

tasks = []


class Task(BaseModel):
    id: int
    caption: str
    text: str
    done: bool


@app.get("/tasks", response_class=HTMLResponse)
async def get_task(request: Request):
    all_tasks = pd.DataFrame([vars(task) for task in tasks]).to_html()

    return templates.TemplateResponse("tasks.html",
                                      {"request": request, "table": all_tasks})


@app.get("/tasks/{id}", response_class=HTMLResponse)
async def get_task(id: int, request: Request):
    all_tasks = pd.DataFrame([vars(tasks[id - 1])]).to_html()

    return templates.TemplateResponse("tasks.html",
                                      {"request": request, "table": all_tasks})


@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task_id = len(tasks) + 1
    task.id = task_id
    task.caption = "Заголовок задачи"
    task.text = "Текст задачи"
    task.done = False
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def put_task(task_id: int, task: Task):
    for i, stored_task in enumerate(tasks):
        if stored_task.id == task_id:
            task.id = task_id
            tasks[i] = task
            return task


@app.delete("/tasks/{task_id}", response_class=HTMLResponse)
async def delete_task(task_id: int):
    for i, stored_task in enumerate(tasks):
        if stored_task.id == task_id:
            return pd.DataFrame([vars(tasks.pop(i))]).to_html()
