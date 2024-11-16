from fastapi import APIRouter
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete

from typing import Annotated
from slugify import slugify

from app.backend.db_depends import get_db
from app.models import *
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task was not found")
    return tasks


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")

    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   user_id=create_task.user_id))

    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int,
                      update_task: UpdateTask):
    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task was not found")

    db.execute(update(Task).where(Task.id == task_id).values(title=update_task.title,
                                                             content=update_task.content,
                                                             priority=update_task.priority))

    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalar(select(Task).where(Task.id == task_id))
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task was not found")

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}



