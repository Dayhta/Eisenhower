from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskList
from sqlalchemy import inspect

def _ensure_new_columns(db: Session):
    """Runtime lightweight migration for new nullable columns (SQLite only)."""
    inspector = inspect(db.bind)
    cols = {c['name'] for c in inspector.get_columns('tasks')}
    new_cols = {
        'impact': 'INTEGER',
        'value_alignment': 'INTEGER',
        'effort': 'INTEGER',
        'due_date': 'TIMESTAMP',
    }
    for name, ddl in new_cols.items():
        if name not in cols:
            db.execute(f'ALTER TABLE tasks ADD COLUMN {name} {ddl}')
    if 'priority_score' not in cols:
        db.execute('ALTER TABLE tasks ADD COLUMN priority_score FLOAT')
    db.commit()

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    _ensure_new_columns(db)
    db_task = Task(
        title=task.title,
        description=task.description,
        urgency=task.urgency,
        importance=task.importance,
        impact=task.impact,
        value_alignment=task.value_alignment,
        effort=task.effort,
        due_date=task.due_date,
    )
    
    # Calculate priority score
    db_task.priority_score = db_task.calculate_priority_score()
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


@router.get("/", response_model=TaskList)
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks ranked by priority score"""
    _ensure_new_columns(db)
    tasks = db.query(Task).order_by(Task.priority_score.desc()).all()
    return TaskList(tasks=tasks, total=len(tasks))


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task"""
    _ensure_new_columns(db)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update fields if provided
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    # Recalculate priority score if urgency or importance changed
    if any(k in update_data for k in ["urgency","importance","impact","value_alignment","effort","due_date"]):
        task.priority_score = task.calculate_priority_score()
    
    db.commit()
    db.refresh(task)
    
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}


@router.get("/matrix/data", response_model=dict)
def get_matrix_data(db: Session = Depends(get_db)):
    """Get tasks organized by Eisenhower Matrix quadrants"""
    _ensure_new_columns(db)
    tasks = db.query(Task).all()
    
    # Organize tasks by quadrants
    # Quadrant 1: Urgent + Important (urgency >= 6, importance >= 6)
    # Quadrant 2: Not Urgent + Important (urgency < 6, importance >= 6)
    # Quadrant 3: Urgent + Not Important (urgency >= 6, importance < 6)
    # Quadrant 4: Not Urgent + Not Important (urgency < 6, importance < 6)
    
    matrix_data = {
        "quadrant_1": [],  # Do First (Urgent + Important)
        "quadrant_2": [],  # Schedule (Not Urgent + Important)
        "quadrant_3": [],  # Delegate (Urgent + Not Important)
        "quadrant_4": []   # Eliminate (Not Urgent + Not Important)
    }
    
    for task in tasks:
        task_data = TaskResponse.model_validate(task)
        
        if task.urgency >= 6 and task.importance >= 6:
            matrix_data["quadrant_1"].append(task_data)
        elif task.urgency < 6 and task.importance >= 6:
            matrix_data["quadrant_2"].append(task_data)
        elif task.urgency >= 6 and task.importance < 6:
            matrix_data["quadrant_3"].append(task_data)
        else:
            matrix_data["quadrant_4"].append(task_data)
    
    return matrix_data
