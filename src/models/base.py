from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime
from config.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class TimeStampedModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creado_en = Column(DateTime, default=utc_now)
    actualizado_en = Column(DateTime, default=utc_now, onupdate=utc_now)