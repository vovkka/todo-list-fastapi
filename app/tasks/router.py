from fastapi import APIRouter, Depends, status, HTTPException

from app.users.dependencies import get_current_user
from app.users.models import Users

from app.tasks.schemas import STaskCreate, STask
from app.tasks.dao import TasksDAO

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_task(task: STaskCreate, user: Users = Depends(get_current_user)):
    await TasksDAO.insert_data(user_id=user.id, name=task.name, description=task.description)
    return {"status": status.HTTP_201_CREATED}


@router.get("/")
async def get_tasks(user: Users = Depends(get_current_user)) -> list[STask]:
    return await TasksDAO.get_all(user_id=user.id)


@router.get("/{task_id}")
async def get_task(task_id: int, user: Users = Depends(get_current_user)) -> STask:
    task_or_none = await TasksDAO.get_one_or_none(id=task_id, user_id=user.id)
    if task_or_none is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return task_or_none


@router.delete("/{task_id}")
async def delete_task(task_id: int, user: Users = Depends(get_current_user)):
    task_or_none = await TasksDAO.get_one_or_none(id=task_id, user_id=user.id)
    if task_or_none is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await TasksDAO.delete(id=task_id, user_id=user.id)
    return {"status": status.HTTP_200_OK}

