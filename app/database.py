from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_engine():
    """
    Returns the SQLAlchemy engine.
    """
    return engine


def get_session():
    """
    Returns a new database session.
    """
    return SessionLocal()