import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.test_database_username}:{settings.test_database_password}@" \
                          f"{settings.test_database_hostname}:{settings.test_database_port}/{settings.test_database_name}"
# when using sqlite database you have to use pass in this arg to the create_engine function
# connect_args={"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# @pytest.fixture()
# def session():
#     print('creating session')
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @pytest.fixture()
# def client(session):
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)
