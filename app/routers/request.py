from app.crud.crud import CRUD
from app.schemas.request_schema import RequestCreate, RequestResponse, RequestUpdate
from app.routers.routes import routes
from app.models import Request

req = CRUD(Request)

router = routes(
    create_func=req.create,
    get_func=req.get,
    update_func=req.update,
    delete_func=req.delete,
    create_schema=RequestCreate,
    response_schema=RequestResponse,
    update_schema=RequestUpdate
)