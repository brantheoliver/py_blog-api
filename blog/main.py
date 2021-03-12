from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from . import schemas
from . import models
from .database import engine, SessionLocal


app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def get_one(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {f"Blog with the id {id} is not available."}
        # this can be replaced by:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available.",
        )
    return blog