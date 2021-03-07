from logging import Logger

from exceptions import CalculateScoreException, GitHubServiceRequestException
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from services.github import GitHubService
from services.popular import PopularService
from starlette import status
from starlette.responses import JSONResponse

router = InferringRouter()

logger = Logger(f"{__name__}")


@cbv(router)
class PopularView:
    def __init__(self, *, github_service=None, popular_service=None):
        self.github_service = github_service or GitHubService()
        self.popular_service = popular_service or PopularService()

    def get_router(self):  # pragma: no cover
        return router

    @router.get("/repository")
    def check(self, repository_name: str):
        try:
            repo_data = self.github_service.get_info(repository_name=repository_name)
            popular_data = self.popular_service.calculate_score(repository_data=repo_data)

            return JSONResponse(content=jsonable_encoder(popular_data), status_code=status.HTTP_200_OK)

        except GitHubServiceRequestException as ex:
            logger.error(f"Error when retrieving repository info, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to get repository info"},
            )
        except CalculateScoreException as ex:
            logger.error(f"Error when calculating score, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to calculate score"},
            )
