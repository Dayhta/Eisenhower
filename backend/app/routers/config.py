from fastapi import APIRouter
from pydantic import BaseModel, Field
from ..settings import get_priority_config, set_priority_overrides, clear_priority_overrides

router = APIRouter(prefix="/config", tags=["config"])


class PriorityOverrides(BaseModel):
    weight_urgency: float | None = Field(None, ge=0, le=1)
    weight_importance: float | None = Field(None, ge=0, le=1)
    weight_impact: float | None = Field(None, ge=0, le=1)
    weight_value: float | None = Field(None, ge=0, le=1)
    effort_penalty: float | None = Field(None, ge=0, le=1)
    due_soon_days: int | None = Field(None, ge=1, le=60)
    due_soon_max_bonus: float | None = Field(None, ge=0, le=1)


@router.get("/priority")
def get_priority_settings():
    """Return the current priority scoring configuration (with any runtime overrides applied)."""
    return get_priority_config()


@router.put("/priority")
def update_priority_settings(payload: PriorityOverrides):
    """Update (override) runtime priority scoring parameters. Persist only in memory until restart."""
    overrides = payload.model_dump(exclude_unset=True)
    cfg = set_priority_overrides(**overrides)
    return cfg


@router.delete("/priority/overrides")
def reset_priority_settings():
    """Clear all runtime overrides, reverting to environment-variable configuration."""
    return clear_priority_overrides()
