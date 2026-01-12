from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class FileInfo(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)

    full_path = Column(String, nullable=False, unique=True)
    file_name = Column(String, nullable=False)
    extension = Column(String, nullable=True)

    size_bytes = Column(BigInteger, nullable=False)

    created_at = Column(DateTime, nullable=True)
    modified_at = Column(DateTime, nullable=False)

    last_scanned_at = Column(DateTime, nullable=False, default=datetime.utcnow)
