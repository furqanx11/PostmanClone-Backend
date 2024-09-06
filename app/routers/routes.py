from fastapi import APIRouter, HTTPException, status, Response
from typing import Type, TypeVar, Callable
from pydantic import BaseModel, ValidationError
from app.exceptions.custom_exceptions import Custom201Response
from app.exceptions.custom_exceptions import CustomValidationException

TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)

def routes(
    create_func: Callable[[dict], TResponseSchema],
    get_func: Callable[[str], TResponseSchema],
    update_func: Callable[[str, dict], TResponseSchema],
    delete_func: Callable[[str], None],
    head_func: Callable[[str], TResponseSchema],
    put_func: Callable[[str, dict], TResponseSchema],
    create_schema: Type[TCreateSchema],
    response_schema: Type[TResponseSchema],
    update_schema: Type[TUpdateSchema] 
) -> APIRouter:
    router = APIRouter() 

    @router.post("/", response_model=response_schema, status_code=status.HTTP_201_CREATED)
    async def create(item: create_schema):
        try:
            item = await create_func(item.dict())
            if not item:
                raise CustomValidationException(status_code=400, detail="Item not created.", pre = True)
            return item
        except ValidationError as e:
            raise CustomValidationException(status_code=400, detail=str(e))

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
            raise HTTPException(status_code=422, detail=str(e))
        
    @router.delete("/{id}", response_model=None)
    async def delete(id: str):
        item_to_delete = await get_func(id)
        if not item_to_delete:
            raise HTTPException(status_code=404, detail="Item not found")
        await delete_func(id)
        return {"detail": "Item deleted successfully"}

    @router.options("/", response_model=None)
    async def options(response: Response):
        response.headers["Allow"] = "OPTIONS, GET, HEAD, POST, PUT, PATCH, DELETE"
        return {"detail": "Options request successful"}

    @router.head("/{id}", response_model=None)
    async def head(id: int):
        item = await head_func(id)
        if not item:
            raise HTTPException(status_code=404)
        return CustomValidationException(status_code=200, detail=None)

    @router.put("/{id}", response_model=response_schema)
    async def put_item(id: str, item: update_schema):
        try:
            item_data = item.dict()  
            for field, value in item_data.items():
                if value is None:
                    raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
            
            updated_item = await put_func(id, item_data)
            if not updated_item:
                raise HTTPException(status_code=404, detail="Item not found")
            return updated_item
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=str(e))

    return router