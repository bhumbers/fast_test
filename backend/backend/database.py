from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///"  # Use SQLite for simplicity

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, 
    connect_args={"check_same_thread": False},  # SQLite-specific
    poolclass=StaticPool
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
