from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, Text, DateTime, Integer
)
from sqlalchemy.dialects import postgresql as pg

from .config import BaseMixin, BaseModel


class Wordle(BaseMixin, BaseModel):    # type: ignore
    id = Column(
        'id', pg.UUID, default=uuid4, nullable=False, primary_key=True)
    seed = Column(Integer, nullable=False)
    word = Column(Text, nullable=False, unique=True)
    length = Column(Integer, nullable=False)
    daily = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
