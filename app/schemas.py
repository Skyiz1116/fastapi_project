from pydantic import BaseModel, Field
from typing import Optional, List

# === КАТЕГОРИИ ===

class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Название категории")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# === КНИГИ ===

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Название книги")
    description: Optional[str] = Field(None, max_length=1000, description="Описание книги")
    price: float = Field(..., gt=0, le=100000, description="Цена книги (должна быть больше 0)")
    url: Optional[str] = Field(None, max_length=500, description="URL книги")
    category_id: int = Field(..., gt=0, description="ID категории (должен быть больше 0)")

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0, le=100000)
    url: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = Field(None, gt=0)

class BookResponse(BookBase):
    id: int
    
    class Config:
        from_attributes = True

class BookWithCategory(BookResponse):
    category: Optional[CategoryResponse] = None