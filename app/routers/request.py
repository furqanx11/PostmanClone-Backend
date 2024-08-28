from app.crud.crud import CRUD
from app.schemas.request_schema import RequestCreate, Request_Response, RequestUpdate
from app.routers.routes import routes
from app.models import Request, Request_Pydantic

req = CRUD(Request, Request_Pydantic)

router = routes(
    create_func=req.create,
    get_func=req.get,
    update_func=req.update,
    delete_func=req.delete,
    create_schema=RequestCreate,
    response_schema=Request_Response,
    update_schema=RequestUpdate
)