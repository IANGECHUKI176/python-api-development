from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[schemas.UserList])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id:{id} not found")
    return user
