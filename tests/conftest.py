import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar la raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, get_db
from app.main import app

# Use SQLite in-memory database for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create test database tables before tests run."""
    # Create all tables in SQLite test database
    Base.metadata.create_all(bind=test_engine)
    yield
    # Clean up: drop all tables and remove test database file
    Base.metadata.drop_all(bind=test_engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(autouse=True)
def override_get_db():
    """Override the get_db dependency to use SQLite test database."""
    def get_test_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()