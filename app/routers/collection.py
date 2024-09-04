from app.crud.crud import CRUD
from app.schemas.collection_schema import CollectionCreate, Collction_Response, CollectionUpdate
from app.routers.routes import routes
from app.models import Collection,Collection_Pydantic, Request, Request_Pydantic, Response, Response_Pydantic, Parameter, Parameter_Pydantic

coll = CRUD(Collection, Collection_Pydantic)


router = routes(
    create_func=coll.create,
    get_func=coll.get,
    update_func=coll.update,
    delete_func=coll.delete,
    create_schema=CollectionCreate,
    response_schema=Collction_Response,
    update_schema=CollectionUpdate
)


async def get_all_collections():
    collections = await coll.get_all_collections_with_nested()
    result = []
    for collection in collections:
        collection_pydantic = await Collection_Pydantic.from_tortoise_orm(collection)
        collection_dict = collection_pydantic.dict()  # Convert Pydantic model to dictionary

        requests = await Request.filter(collection_id=collection.id).all()
        requests_list = []
        for request in requests:
            request_pydantic = await Request_Pydantic.from_tortoise_orm(request)
            request_dict = request_pydantic.dict()

            params = await Parameter.filter(request_id=request.id).all()
            request_dict['params'] = [await Parameter_Pydantic.from_tortoise_orm(param) for param in params]

            responses = await Response.filter(request_id=request.id).all()
            request_dict['responses'] = [await Response_Pydantic.from_tortoise_orm(response) for response in responses]

            requests_list.append(request_dict)

        collection_dict['requests'] = requests_list
        result.append(collection_dict)
    return result