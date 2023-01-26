from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# when using sqlite database you have to use pass in this arg to the create_engine function
# connect_args={"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    connection = psycopg2.connect(user=settings.database_username,
                                  password=settings.database_password,
                                  host=settings.database_hostname,
                                  port=settings.database_port,
                                  database=settings.database_name,
                                  cursor_factory=RealDictCursor
                                  )
    cursor = connection.cursor()

    print('connected to database')

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
