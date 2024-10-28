from fastapi import APIRouter, Depends, HTTPException, status, Path
from app.config import get_db
from sqlalchemy.orm import Session
from app.schemas import RequestTask, ResponseTask, ListResponseTask
from app.crud import get_tasks_manage, create_task_manage, get_task_by_id, update_task_manage, delete_task_manage

router = APIRouter(
    prefix="/tasks",
)


@router.get("/", response_model=ListResponseTask)
def get_tasks(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    tasks = get_tasks_manage(db, skip=skip, limit=limit)
    return {"code": "success", "status": status.HTTP_200_OK, "response": tasks}


@router.post("/", response_model=ResponseTask, status_code=status.HTTP_201_CREATED)
def create_task(task: RequestTask, db: Session = Depends(get_db)):
    create_task_manage(db, task)
    return {"code": "success", "status": status.HTTP_201_CREATED, "response": task}


@router.get("/{task_id}", response_model=ResponseTask)
def retrieve_task(task_id: int = Path(...), db: Session = Depends(get_db)):
    db_task = get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_task}


@router.put("/{task_id}", response_model=ResponseTask)
def update_task(task_id: int = Path(...), task: RequestTask = None, db: Session = Depends(get_db)):
    db_task = get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    update_task_manage(db, task_id=task_id, task=task)
    return {"code": "success", "status": status.HTTP_200_OK, "response": db_task}


@router.delete("/{task_id}", response_model=ResponseTask)
def delete_task(task_id: int = Path(...), db: Session = Depends(get_db)):
    db_task = get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    delete_task_manage(db, task_id=task_id)
    return {"code": "success", "status": status.HTTP_204_NO_CONTENT, "response": "task deleted"}
