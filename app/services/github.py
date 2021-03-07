import logging

import requests
from config import GITHUB_API_ACCESS_TOKEN, GITHUB_API_URL
from exceptions import (
    GitHubServiceRequestException,
    RepositoryForbiddenException,
    RepositoryMovedPermanently,
    RepositoryNameException,
    RepositoryNotFoundException,
)
from schemas.github import GitHupApiResponse
from starlette import status

logger = logging.getLogger(__name__)


class GitHubService:
    def __init__(self, *, url=None, access_token=None):
        self.url = url or GITHUB_API_URL
        self.access_token = access_token or GITHUB_API_ACCESS_TOKEN

    def get_info(self, repository_name: str) -> GitHupApiResponse:
        try:
            owner, repository = repository_name.split("/")
        except ValueError as ex:
            logger.error(f"Error: repository_name {repository_name}" f" could not be parsed. ex: {ex}")
            raise RepositoryNameException
        try:
            response = requests.get(
                url=f"{self.url}/repos/{owner}/{repository}", headers={"Authorization": f"token {self.access_token}"}
            )
        except Exception as ex:
            logger.error(f"An unexpected error occurred." f" ex: {ex}")
            raise GitHubServiceRequestException

        if response.status_code == status.HTTP_404_NOT_FOUND:
            logger.info(f"Repository: {repository_name} not found")
            raise RepositoryNotFoundException

        if response.status_code == status.HTTP_403_FORBIDDEN:
            logger.error("Error: Request forbidden. Please check you access token")
            raise RepositoryForbiddenException

        if response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            logger.error("Error: Moved permanently")
            raise RepositoryMovedPermanently

        if response.status_code != status.HTTP_200_OK:
            logger.error(f"An unexpected error occurred." f" status: {response.status_code}")
            raise GitHubServiceRequestException

        data = response.json()

        return GitHupApiResponse(
            stars=data["stargazers_count"], forks=data["forks_count"], owner=owner, name=repository
        )
