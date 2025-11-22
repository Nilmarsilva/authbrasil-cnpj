"""
Plan Model
Subscription plans configuration
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class Plan(Base):
    """Plans table - Available subscription tiers"""
    
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Starter, Pro, Enterprise
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  # Monthly price in BRL
    query_limit = Column(Integer, nullable=False)  # Monthly query limit
    stripe_price_id = Column(String, nullable=True)  # Stripe Price ID
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="plan")
