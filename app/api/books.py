from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app import schemas

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[schemas.BookWithCategory])
def get_books(
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    """Получить список книг (можно фильтровать по category_id)"""
    return crud.get_books(db, skip=skip, limit=limit, category_id=category_id)

@router.get("/{book_id}", response_model=schemas.BookWithCategory)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=schemas.BookWithCategory, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    # Проверяем существование категории
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return crud.create_book(db, book)

@router.put("/{book_id}", response_model=schemas.BookWithCategory)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу"""
    # Если меняем категорию, проверяем её существование
    if book.category_id:
        category = crud.get_category(db, book.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    updated = crud.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    success = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None