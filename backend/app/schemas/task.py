from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    urgency: int = Field(..., ge=1, le=10)
    importance: int = Field(..., ge=1, le=10)
    impact: Optional[int] = Field(5, ge=1, le=10)
    value_alignment: Optional[int] = Field(5, ge=1, le=10)
    effort: Optional[int] = Field(5, ge=1, le=10)
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    urgency: Optional[int] = Field(None, ge=1, le=10)
    importance: Optional[int] = Field(None, ge=1, le=10)
    impact: Optional[int] = Field(None, ge=1, le=10)
    value_alignment: Optional[int] = Field(None, ge=1, le=10)
    effort: Optional[int] = Field(None, ge=1, le=10)
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    urgency: int
    importance: int
    impact: Optional[int]
    value_alignment: Optional[int]
    effort: Optional[int]
    due_date: Optional[datetime]
    priority_score: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: list[TaskResponse]
    total: int
