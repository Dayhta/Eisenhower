"""Application settings and priority scoring configuration.

Environment overrides (optional):
  WEIGHT_URGENCY, WEIGHT_IMPORTANCE, WEIGHT_IMPACT, WEIGHT_VALUE
  EFFORT_PENALTY, DUE_SOON_DAYS, DUE_SOON_MAX_BONUS

Weights need not sum to 1; they'll be normalized in scoring.
"""
from __future__ import annotations
from functools import lru_cache
import os

# In-memory runtime overrides (not persisted). These override env values if set.
_RUNTIME_OVERRIDES: dict[str, float | int] = {}

@lru_cache
def get_priority_config():
    def _f(name: str, default: float) -> float:
        try:
            return float(os.getenv(name, default))
        except ValueError:
            return default
    base = {
        "weight_urgency": _f("WEIGHT_URGENCY", 0.30),
        "weight_importance": _f("WEIGHT_IMPORTANCE", 0.30),
        "weight_impact": _f("WEIGHT_IMPACT", 0.20),
        "weight_value": _f("WEIGHT_VALUE", 0.20),
        "effort_penalty": _f("EFFORT_PENALTY", 0.15),  # factor per normalized effort unit
        "due_soon_days": int(os.getenv("DUE_SOON_DAYS", 5)),
        "due_soon_max_bonus": _f("DUE_SOON_MAX_BONUS", 0.15),  # multiplicative bonus cap
    }
    # Apply runtime overrides
    for k, v in _RUNTIME_OVERRIDES.items():
        if k in base:
            base[k] = v
    return base

def refresh_priority_config():  # pragma: no cover
    get_priority_config.cache_clear()
    return get_priority_config()


def set_priority_overrides(**overrides):  # pragma: no cover - simple helper
    """Set runtime overrides for priority configuration.
    Only known keys are accepted. Call refresh_priority_config afterwards to apply."""
    valid = get_priority_config().keys()  # ensures base initialized
    for k, v in overrides.items():
        if k in valid and v is not None:
            _RUNTIME_OVERRIDES[k] = v
    refresh_priority_config()
    return get_priority_config()


def clear_priority_overrides():  # pragma: no cover
    _RUNTIME_OVERRIDES.clear()
    refresh_priority_config()
    return get_priority_config()
