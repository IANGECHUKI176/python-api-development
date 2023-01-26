from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),
         current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_post = vote_query.first()
    if vote.dir == 1:
        if found_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with id:{current_user.id}"
                                       f" already voted for post with id:{vote.post_id}")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote created"}
    else:
        if not found_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id:{vote.post_id} not found")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote deleted"}
