import datetime
import logging
from fastapi import APIRouter, HTTPException
from typing import Type, TypeVar, Callable
from pydantic import BaseModel, ValidationError

TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)

def routes(
    create_func: Callable[[dict], TResponseSchema],
    get_func: Callable[[str], TResponseSchema],
    update_func: Callable[[str, dict], TResponseSchema],
    delete_func: Callable[[str], None],
    create_schema: Type[TCreateSchema],
    response_schema: Type[TResponseSchema],
    update_schema: Type[TUpdateSchema] 
) -> APIRouter:
    router = APIRouter() 

    @router.post("/", response_model=response_schema)
    async def create(item: create_schema):
        item = await create_func(item.dict())
        return item    

    @router.get("/{id}", response_model=response_schema)
    async def read(id: str):
        item = await get_func(id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    

    @router.patch("/{id}", response_model=response_schema)
    async def update_item(id: int, item: update_schema):
        try:
            item_data = item.dict(exclude_unset=True)
            updated_item = await update_func(id, item_data)
            if not updated_item:
                raise HTTPException(status_code=404, detail="Item not found")
            return updated_item
        except ValidationError as e:
            logging.error(f"Validation error: {e}")
            raise HTTPException(status_code=422, detail=str(e))
        
    @router.delete("/{id}", response_model=None)
    async def delete(id: str):
        item_to_delete = await get_func(id)
        if not item_to_delete:
            raise HTTPException(status_code=404, detail="Item not found")
        await delete_func(id)
        return {"detail": "Item deleted successfully"}

    return router