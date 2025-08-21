from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine
from app.settings import clear_priority_overrides

client = TestClient(app)


def setup_module(_):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    clear_priority_overrides()


def create_sample_task(urgency=5, importance=5, impact=5, value_alignment=5, effort=5, due_offset_hours=2):
    due = (datetime.now(timezone.utc) + timedelta(hours=due_offset_hours)).isoformat()
    payload = {
        "title": f"Task u{urgency}i{importance}",
        "description": "sample",
        "urgency": urgency,
        "importance": importance,
        "impact": impact,
        "value_alignment": value_alignment,
        "effort": effort,
        "due_date": due,
    }
    r = client.post("/api/tasks/", json=payload)
    assert r.status_code == 200, r.text
    return r.json()


def test_create_and_list_tasks():
    t1 = create_sample_task(urgency=9, importance=9)
    t2 = create_sample_task(urgency=3, importance=4)
    r = client.get("/api/tasks/")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 2
    assert t1["priority_score"] >= t2["priority_score"]


def test_matrix_endpoint_classification():
    create_sample_task(urgency=9, importance=9)  # Q1
    create_sample_task(urgency=2, importance=9)  # Q2
    create_sample_task(urgency=9, importance=2)  # Q3
    create_sample_task(urgency=2, importance=1)  # Q4
    r = client.get("/api/tasks/matrix/data")
    assert r.status_code == 200
    data = r.json()
    for q in ["quadrant_1", "quadrant_2", "quadrant_3", "quadrant_4"]:
        assert len(data[q]) >= 1


def test_update_recalculates_score():
    task = create_sample_task(urgency=4, importance=4)
    original = task["priority_score"]
    r = client.put(f"/api/tasks/{task['id']}", json={"urgency": 10})
    assert r.status_code == 200
    updated = r.json()
    assert updated["priority_score"] >= original


def test_runtime_config_override_endpoint():
    r = client.get("/api/config/priority")
    assert r.status_code == 200
    base_weight = r.json()["weight_urgency"]

    r2 = client.put("/api/config/priority", json={"weight_urgency": base_weight + 0.05})
    assert r2.status_code == 200
    assert abs(r2.json()["weight_urgency"] - (base_weight + 0.05)) < 1e-6

    r3 = client.delete("/api/config/priority/overrides")
    assert r3.status_code == 200
    assert r3.json()["weight_urgency"] == base_weight
