from app.crud.crud import CRUD
from app.schemas.response_schema import ResponseCreate, ResponseResponse, ResponseUpdate
from app.routers.routes import routes
from app.models import Response, Response_Pydantic

res = CRUD(Response, Response_Pydantic)

router = routes(
    create_func=res.create,
    get_func=res.get,
    update_func=res.update_partial,
    delete_func=res.delete,
    put_func=res.update_full,
    head_func=res.head,
    create_schema=ResponseCreate,
    response_schema=ResponseResponse,
    update_schema=ResponseUpdate
)