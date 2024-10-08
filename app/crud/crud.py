from typing import Any, Dict, List, Optional, TypeVar
from app.models import Collection
from tortoise.models import Model
from app.exceptions.custom_exceptions import CustomValidationException

TModel = TypeVar("TModel", bound=Model)

class CRUD:
    def __init__(self, model: TModel, model_pydantic):
        self.model = model
        self.model_pydantic = model_pydantic

    async def create(self, item_data: Dict[str, Any]) -> TModel:
        try:
            item = await self.model.create(**item_data)
            return item
        except Exception as e:
            raise CustomValidationException(status_code=400, detail=str(e))

    async def get(self, id: int) -> Optional[Dict[str, Any]]:
        item = await self.model.filter(id=id).values()
        if not item:
            raise CustomValidationException(status_code=404, detail=f"{self.model.__name__} with id {id} does not exist.")
        
        return item[0]
    
    async def update_partial(self, id: int, item_data: Dict[str, Any]) -> Optional[TModel]:
        update_data = {k: v for k, v in item_data.items() if v is not None}
        if not update_data:
            raise CustomValidationException(status_code=400, detail="No valid fields provided for update.")

        await self.model.filter(id=id).update(**update_data)

        item = await self.model.filter(id=id).first()
        if item is None:
            raise CustomValidationException(status_code=404, detail=f"{self.model.__name__} with id {id} does not exist.")
        return item

    async def update_full(self, id: int, item_data: Dict[str, Any]) -> Optional[TModel]:
        await self.model.filter(id=id).update(**item_data)
        item = await self.model.filter(id=id).first()
        if item is None:
            raise CustomValidationException(status_code=404, detail=f"{self.model.__name__} with id {id} does not exist.")
        return item


    async def delete(self, id: int) -> None:
        await self.model.filter(id=id).delete()
    
    async def get_all_collections_with_nested(self) -> List[Collection]:
        collections = await Collection.all().prefetch_related('requests__parameters', 'requests__responses')
        return collections
    
    async def head(self, id: int) -> None:
        item = await self.model.filter(id=id).values()
        if not item:
            return False
        
        return True