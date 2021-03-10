import json
from logging import Logger

from exceptions import (
    CalculateScoreException,
    GitHubServiceRequestException,
    RepositoryNameException,
    RequestForbiddenException,
    RequestMovedPermanently,
    RequestNotFoundException,
)
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from schemas.popular import PopularResponseListModel, PopularResponseModel
from services.cache import CacheService
from services.github import GitHubService
from services.popular import PopularService
from starlette import status
from starlette.responses import JSONResponse

router = InferringRouter()

logger = Logger(f"{__name__}")


@cbv(router)
class PopularView:
    def __init__(self, *, github_service=None, popular_service=None, cache_service=None):
        self.github_service = github_service or GitHubService()
        self.popular_service = popular_service or PopularService()
        self.cache_service = cache_service or CacheService()

    def get_router(self):  # pragma: no cover
        return router

    @router.get("/repository", response_model=PopularResponseModel)
    def check(self, repository_name: str):
        try:
            cache_value = self.cache_service.check(key=repository_name)

            if cache_value:
                cache_data = json.loads(cache_value)
                return JSONResponse(content=cache_data, status_code=status.HTTP_200_OK)

            repo_data = self.github_service.get_info(repository_name=repository_name)
            popular_data = self.popular_service.calculate_score(repository_data=repo_data)
            self.cache_service.set_key(key=repository_name, value=popular_data.dict())

            return JSONResponse(content=jsonable_encoder(popular_data), status_code=status.HTTP_200_OK)

        except RequestNotFoundException as ex:
            msg = f"repository {repository_name} not found"
            logger.error(f"{msg}, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"title": "Error", "message": msg},
            )

        except RepositoryNameException as ex:
            msg = "An error occurred when trying to parse repository name"
            logger.error(f"{msg}, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": msg},
            )

        except RequestForbiddenException as ex:
            logger.error(f"Error when retrieving repository info, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to get repository info"},
            )

        except RequestMovedPermanently as ex:
            logger.error(f"Error when retrieving repository info, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to get repository info"},
            )

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

    @router.get("/org", response_model=PopularResponseListModel)
    def check_org(self, org_name: str):
        try:
            cache_value = self.cache_service.check(key=org_name)

            if cache_value:
                cache_data = json.loads(cache_value)
                return JSONResponse(content=cache_data, status_code=status.HTTP_200_OK)

            response_data = []
            repos_data = self.github_service.get_org_info(org_name=org_name)

            for repo in repos_data.items:
                popular_data = self.popular_service.calculate_score(repository_data=repo)
                response_data.append(popular_data)

            pop_list_response = PopularResponseListModel(items=response_data)

            self.cache_service.set_key(key=org_name, value=pop_list_response.dict())

            return JSONResponse(content=jsonable_encoder(pop_list_response), status_code=status.HTTP_200_OK)
        except RequestNotFoundException as ex:
            msg = f"org {org_name} not found"
            logger.error(f"{msg}, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"title": "Error", "message": msg},
            )

        except RepositoryNameException as ex:
            msg = "An error occurred when trying to parse repository name"
            logger.error(f"{msg}, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": msg},
            )

        except RequestForbiddenException as ex:
            logger.error(f"Error when retrieving org info, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to get org info"},
            )

        except RequestMovedPermanently as ex:
            logger.error(f"Error when retrieving org info, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to get org info"},
            )

        except GitHubServiceRequestException as ex:
            logger.error(f"Error when retrieving org info, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to get org info"},
            )
        except CalculateScoreException as ex:
            logger.error(f"Error when calculating score, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "An error occurred when trying to calculate score"},
            )
