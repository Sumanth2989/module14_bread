import sys
from pathlib import Path
import pytest

# Ensure project root is on sys.path so "import app" works in tests
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from app.db import get_db

@pytest.fixture
def db_session():
    """
    Provides a database session for E2E tests.
    Uses the same Session as the app via get_db().
    """
    db = next(get_db())  # ✅ get actual Session object
    try:
        yield db
    finally:
        db.close()
