# from fastapi import FastAPI, HTTPException, APIRouter
# from pydantic import BaseModel
# from typing import Optional
# from tortoise import fields, models, Tortoise
# from tortoise.contrib.pydantic import pydantic_model_creator
# from tortoise.contrib.fastapi import register_tortoise

# # Define the Tortoise ORM model
# class Collection(models.Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255)
#     description = fields.TextField(null=True)
#     created_at = fields.DatetimeField(auto_now_add=True)
#     updated_at = fields.DatetimeField(auto_now=True)

# class CollectionUpdate(BaseModel):
#     name: str
#     description: Optional[str] = None

# # Create Pydantic models for serialization
# Collection_Pydantic = pydantic_model_creator(Collection, name="Collection")
# CollectionIn_Pydantic = pydantic_model_creator(Collection, name="CollectionIn", exclude_readonly=True)

# # Define the update model with optional fields, except 'name' is required

# # Create the FastAPI app and router
# app = FastAPI()
# router = APIRouter()

# # CRUD operations

# # Create a new collection
# @router.post("/collection", response_model=Collection_Pydantic)
# async def create_collection(collection: CollectionIn_Pydantic):
#     db_collection = await Collection.create(**collection.dict())
#     return await Collection_Pydantic.from_tortoise_orm(db_collection)

# # Read a collection by ID
# @router.get("/collection/{collection_id}", response_model=Collection_Pydantic)
# async def get_collection(collection_id: int):
#     collection = await Collection.get(id=collection_id)
#     if not collection:
#         raise HTTPException(status_code=404, detail="Collection not found")
#     return await Collection_Pydantic.from_tortoise_orm(collection)

# # Update a collection by ID
# @router.patch("/collection/{collection_id}", response_model=Collection_Pydantic)
# async def update_collection(collection_id: int, collection: Collection_Pydantic):
#     try:
#         db_collection = await Collection.get(id=collection_id)
#     except Collection.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Collection not found")

#     # Filter out None or empty fields
#     update_data = {key: value for key, value in collection.dict(exclude_unset=True).items() if value not in [None, ""]}

#     # Update only the fields that are provided
#     if update_data:
#         db_collection.update_from_dict(update_data)
#         await db_collection.save()

#     return await Collection_Pydantic.from_tortoise_orm(db_collection)

# # Delete a collection by ID
# @router.delete("/collection/{collection_id}")
# async def delete_collection(collection_id: int):
#     try:
#         collection = await Collection.get(id=collection_id)
#     except Collection.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Collection not found")
#     await collection.delete()
#     return {"message": "Collection deleted successfully"}

# # Register the router
# app.include_router(router)

# # Configure Tortoise ORM
# Tortoise.init_models(["__main__"], "models")

# register_tortoise(
#     app,
#     db_url="postgres://furqan:1234@localhost:5432/postmanDB",  # Use SQLite for testing; replace with your actual DB URL
#     modules={"models": ["__main__"]},
#     generate_schemas=True,
#     add_exception_handlers=True,
# )

# # Main method to run the FastAPI app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=7000)


from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise

# Define the Tortoise ORM model
class Collection(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

# Create Pydantic models for serialization
Collection_Pydantic = pydantic_model_creator(Collection, name="Collection")
CollectionIn_Pydantic = pydantic_model_creator(Collection, name="CollectionIn", exclude_readonly=True)

# Define the update model with optional fields, except 'name' is required
class CollectionUpdate(BaseModel):
    name: str
    description: Optional[str] = None

# Create the FastAPI app and router
app = FastAPI()
router = APIRouter()

# CRUD operations

# Create a new collection
@router.post("/collection", response_model=Collection_Pydantic)
async def create_collection(collection: CollectionIn_Pydantic):
    db_collection = await Collection.create(**collection.dict())
    return await Collection_Pydantic.from_tortoise_orm(db_collection)

# Read a collection by ID
@router.get("/collection/{collection_id}", response_model=Collection_Pydantic)
async def get_collection(collection_id: int):
    collection = await Collection.get(id=collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return await Collection_Pydantic.from_tortoise_orm(collection)

# Update a collection by ID
@router.patch("/collection/{collection_id}", response_model=Collection_Pydantic)
async def update_collection(collection_id: int, collection: CollectionUpdate):
    try:
        db_collection = await Collection.get(id=collection_id)
    except Collection.DoesNotExist:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Filter out None or empty fields
    update_data = collection.dict(exclude_unset=True)
    print(update_data)

    # Update only the fields that are provided
    if update_data:
        db_collection.update_from_dict(update_data)
        await db_collection.save()

    return await Collection_Pydantic.from_tortoise_orm(db_collection)

# Delete a collection by ID
@router.delete("/collection/{collection_id}")
async def delete_collection(collection_id: int):
    try:
        collection = await Collection.get(id=collection_id)
    except Collection.DoesNotExist:
        raise HTTPException(status_code=404, detail="Collection not found")
    await collection.delete()
    return {"message": "Collection deleted successfully"}

# Register the router
app.include_router(router)

# Configure Tortoise ORM
Tortoise.init_models(["__main__"], "models")

register_tortoise(
    app,
    db_url="postgres://furqan:1234@localhost:5432/postmanDB",  # Use SQLite for testing; replace with your actual DB URL
    modules={"models": ["__main__"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Main method to run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7000)