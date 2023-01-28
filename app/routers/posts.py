from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, database, oauth2
from sqlalchemy import func

# connection = database.connection
# cursor = database.cursor

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


# @router.get("/sqlalchemy")
# def test_posts():
#     cursor.execute("""SELECT p.*,COUNT(v.user_id) as total_votes FROM posts p
#     LEFT JOIN votes v ON p.id =v.post_id GROUP BY p.id""")
#     posts = cursor.fetchall()
#     return posts


@router.get('/', response_model=list[schemas.PostVotes])
def get_posts(db: Session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: str | None = "",
              ):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *;""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    # db refresh returns the new post
    db.refresh(new_post)
    return new_post


@router.get('/{id}')
def get_post(id: int, db: Session = Depends(get_db),
             current_user: dict = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (id,))
    # post = cursor.fetchone()
    if results is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")
    return results.first()
    # return results


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db),
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id =%s RETURNING *;""", (id,))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    # using next function -> next((index for index, post in enumerate(posts) if post["id"] == id), None)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="you can only delete your own posts")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
def updated_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                  current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s, published=%s WHERE id=%s RETURNING *;""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_update = post_query.first()
    if post_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} not found")

    if post_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="you can only update your own posts")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
