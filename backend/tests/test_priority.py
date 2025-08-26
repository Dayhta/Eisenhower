from datetime import datetime, timedelta, timezone

from app.models.task import Task
from app.settings import set_priority_overrides, clear_priority_overrides, get_priority_config


def test_basic_scoring_increases_with_urgency_importance():
    low = Task(urgency=1, importance=1)
    high = Task(urgency=10, importance=10)
    assert high.calculate_priority_score() > low.calculate_priority_score()


def test_effort_penalty_reduces_score():
    base = Task(urgency=8, importance=8, effort=1)
    heavy = Task(urgency=8, importance=8, effort=10)
    assert heavy.calculate_priority_score() < base.calculate_priority_score()


def test_due_date_bonus_applies():
    soon = Task(urgency=5, importance=5, due_date=datetime.now(timezone.utc) + timedelta(hours=1))
    later = Task(urgency=5, importance=5, due_date=datetime.now(timezone.utc) + timedelta(days=30))
    assert soon.calculate_priority_score() >= later.calculate_priority_score()


def test_runtime_override_changes_config():
    original = get_priority_config()["weight_urgency"]
    set_priority_overrides(weight_urgency=0.5)
    assert get_priority_config()["weight_urgency"] == 0.5
    clear_priority_overrides()
    assert get_priority_config()["weight_urgency"] == original
