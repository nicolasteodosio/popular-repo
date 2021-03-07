from logging import Logger

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette import status
from starlette.responses import JSONResponse

router = InferringRouter()

logger = Logger(f"{__name__}")


@cbv(router)
class UtilsView:
    def get_router(self):  # pragma: no cover
        return router

    @router.get("/healthcheck")
    def health_check(self):
        return JSONResponse(content={"message": "I'm alive"}, status_code=status.HTTP_200_OK)
