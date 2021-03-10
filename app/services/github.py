import logging

import requests
from config import GITHUB_API_ACCESS_TOKEN, GITHUB_API_URL
from exceptions import (
    GitHubServiceRequestException,
    RepositoryNameException,
    RequestForbiddenException,
    RequestMovedPermanently,
    RequestNotFoundException,
)
from schemas.github import GitHupApiOrgResponse, GitHupApiResponse
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

        self.check_response_status(kind="Repository", name=repository_name, response=response)

        data = response.json()

        return GitHupApiResponse(
            stars=data["stargazers_count"], forks=data["forks_count"], owner=owner, name=repository
        )

    def check_response_status(self, kind: str, name: str, response):
        if response.status_code == status.HTTP_404_NOT_FOUND:
            logger.info(f"{kind}: {name} not found")
            raise RequestNotFoundException
        if response.status_code == status.HTTP_403_FORBIDDEN:
            logger.error("Error: Request forbidden. Please check you access token")
            raise RequestForbiddenException
        if response.status_code == status.HTTP_301_MOVED_PERMANENTLY:
            logger.error("Error: Moved permanently")
            raise RequestMovedPermanently
        if response.status_code != status.HTTP_200_OK:
            logger.error(f"An unexpected error occurred." f" status: {response.status_code}")
            raise GitHubServiceRequestException

    def get_org_info(self, org_name: str):
        try:
            response = requests.get(
                url=f"{self.url}/orgs/{org_name}/repos", headers={"Authorization": f"token {self.access_token}"}
            )

        except Exception as ex:
            logger.error(f"An unexpected error occurred." f" ex: {ex}")
            raise GitHubServiceRequestException

        self.check_response_status(kind="Org", name=org_name, response=response)

        all_data = response.json()
        org_items = []

        for data in all_data:
            org_items.append(
                GitHupApiResponse(
                    stars=data["stargazers_count"], forks=data["forks_count"], owner=org_name, name=data["name"]
                )
            )

        return GitHupApiOrgResponse(items=org_items)
