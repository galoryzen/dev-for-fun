import sys
import os
import pytest

# Agregar la raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables before tests run."""
    Base.metadata.create_all(bind=engine)
    yield