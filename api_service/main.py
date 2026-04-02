"""
Простой REST API для управления задачами.
Документация генерируется автоматически через FastAPI.
"""

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Создание приложения
app = FastAPI(
    title="Task Manager API",
    description="API для управления списком задач",
    version="2.0.0",
    contact={
        "name": "Support Team",
        "email": "support@example.com"
    }
)

# Модели данных
class Task(BaseModel):
    """Модель задачи."""
    id: int
    title: str
    completed: bool = False
    created_at: datetime = datetime.now()

class TaskCreate(BaseModel):
    """Модель для создания задачи."""
    title: str

class TaskUpdate(BaseModel):
    """Модель для обновления задачи."""
    title: Optional[str] = None
    completed: Optional[bool] = None

# Хранилище задач (в памяти)
tasks_db = []
next_id = 1


def verify_api_key(x_api_key: str = Header(...)):
    """Проверка API ключа."""
    valid_keys = ["test-key-123", "prod-key-456"]
    if x_api_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key


@app.get("/tasks", response_model=List[Task])
async def get_tasks(api_key: str = Header(...)):
    """
    Получить список всех задач.

    Возвращает массив всех задач пользователя.
    """
    verify_api_key(api_key)
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, api_key: str = Header(...)):
    """
    Получить задачу по ID.

    - **task_id**: ID задачи
    """
    verify_api_key(api_key)
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate, api_key: str = Header(...)):
    """
    Создать новую задачу.

    - **title**: Название задачи (обязательно)
    """
    global next_id
    verify_api_key(api_key)
    
    new_task = Task(
        id=next_id,
        title=task.title,
        completed=False
    )
    tasks_db.append(new_task)
    next_id += 1
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate, api_key: str = Header(...)):
    """
    Обновить существующую задачу.

    - **task_id**: ID задачи
    - **title**: Новое название (опционально)
    - **completed**: Новый статус (опционально)
    """
    verify_api_key(api_key)
    
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            if task_update.title is not None:
                tasks_db[i].title = task_update.title
            if task_update.completed is not None:
                tasks_db[i].completed = task_update.completed
            return tasks_db[i]
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, api_key: str = Header(...)):
    """
    Удалить задачу по ID.

    - **task_id**: ID задачи для удаления
    """
    verify_api_key(api_key)
    
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)