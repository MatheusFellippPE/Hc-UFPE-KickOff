import pytest
from starlette.testclient import TestClient

@pytest.fixture(scope="session")
def app_client(tmp_path_factory, monkeypatch):
    db_dir = tmp_path_factory.mktemp("db")
    db_path = db_dir / "test.db"
    db_url = f"sqlite:///{db_path.as_posix()}"

    monkeypatch.setenv("DATABASE_URL", db_url)
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret")

    import main
    from database import Base, engine

    Base.metadata.create_all(bind=engine)

    with TestClient(main.app) as client:
        yield client