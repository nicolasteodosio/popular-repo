import logging

import requests
from config import GITHUB_API_ACCESS_TOKEN, GITHUB_API_URL
from exceptions import GitHubServiceRequestException
from schemas.github import GitHupApiResponse

logger = logging.getLogger(__name__)


class GitHubService:
    def __init__(self, *, url=None, access_token=None):
        self.url = url or GITHUB_API_URL
        self.access_token = access_token or GITHUB_API_ACCESS_TOKEN

    def get_info(self, repository_name: str) -> GitHupApiResponse:
        try:
            owner, repository = repository_name.split("/")
            response = requests.get(
                url=f"{self.url}/repos/{owner}/{repository}", headers={"Authorization": f"token {self.access_token}"}
            )
            data = response.json()

            return GitHupApiResponse(
                stars=data["stargazers_count"], forks=data["forks_count"], owner=owner, name=repository
            )
        except Exception as ex:
            logger.error(f"Error getting product info ex: {ex}")
            raise GitHubServiceRequestException(ex)
