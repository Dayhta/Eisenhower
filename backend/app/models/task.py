from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timezone
from ..settings import get_priority_config


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    urgency = Column(Integer, nullable=False)  # 1-10 scale
    importance = Column(Integer, nullable=False)  # 1-10 scale
    impact = Column(Integer, nullable=True)  # 1-10 scale
    value_alignment = Column(Integer, nullable=True)  # 1-10 scale
    effort = Column(Integer, nullable=True)  # 1-10 scale (higher = more cost)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority_score = Column(Float, nullable=True)  # 0-100 scaled
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to user
    owner = relationship("User", back_populates="tasks")
    
    def calculate_priority_score(self):
        """Compute advanced priority score.

        Drivers: urgency, importance, impact, value_alignment (positive)
        Effort: penalizes score
        Due date: bonus if within configured soon window
        Output scaled 0..100 and rounded to 2 decimals.
        """
        cfg = get_priority_config()

        def norm(val):
            if val is None:
                return None
            return (val - 1) / 9 if 1 <= val <= 10 else 0.0

        u = norm(self.urgency)
        imp = norm(self.importance)
        impact = norm(self.impact)
        value = norm(self.value_alignment)
        eff = norm(self.effort)

        weights = {
            'urgency': cfg['weight_urgency'] if u is not None else 0,
            'importance': cfg['weight_importance'] if imp is not None else 0,
            'impact': cfg['weight_impact'] if impact is not None else 0,
            'value': cfg['weight_value'] if value is not None else 0,
        }
        total_w = sum(weights.values()) or 1.0
        base = 0.0
        if u is not None: base += u * weights['urgency']
        if imp is not None: base += imp * weights['importance']
        if impact is not None: base += impact * weights['impact']
        if value is not None: base += value * weights['value']
        base /= total_w

        if eff is not None:
            base *= (1 - cfg['effort_penalty'] * eff)

        if self.due_date and self.due_date.tzinfo is not None:
            now = datetime.now(timezone.utc)
            remaining = (self.due_date - now).total_seconds()
            if remaining > 0:
                days = remaining / 86400
                if days <= cfg['due_soon_days']:
                    bonus = (1 - days / cfg['due_soon_days']) * cfg['due_soon_max_bonus']
                    if bonus > 0:
                        base *= (1 + min(bonus, cfg['due_soon_max_bonus']))

        score = max(0.0, min(base * 100, 100))
        return round(score, 2)
