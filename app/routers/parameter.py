from app.crud.crud import CRUD
from app.schemas.parameter_schema import ParameterCreate, ParameterResponse, ParameterUpdate
from app.routers.routes import routes
from app.models import Parameter

param = CRUD(Parameter)

router = routes(
    create_func=param.create,
    get_func=param.get,
    update_func=param.update,
    delete_func=param.delete,
    create_schema=ParameterCreate,
    response_schema=ParameterResponse,
    update_schema=ParameterUpdate
)