import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Configuration ---
DB_HOST = os.environ.get('RDS_HOSTNAME', 'localhost')
DB_PORT = os.environ.get('RDS_PORT', '5432')
DB_USER = os.environ.get('RDS_USERNAME', 'postgres')
DB_PASSWORD = os.environ.get('RDS_PASSWORD', 'postgres')
DB_NAME = os.environ.get('RDS_DB_NAME', 'blacklistdb')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
