from logging import Logger

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()

logger = Logger(f"{__name__}")


@cbv(router)
class UtilsView:
    def get_router(self):  # pragma: no cover
        return router

    @router.get("/healthcheck")
    async def health_check(self):
        return {"message": "I'm alive"}
