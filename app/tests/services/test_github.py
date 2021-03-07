import pytest
from config import GITHUB_API_ACCESS_TOKEN, GITHUB_API_URL
from exceptions import GitHubServiceRequestException
from schemas.github import GitHupApiResponse
from services.github import GitHubService


def test_get_info(requests_mock):
    requests_mock.get(f"{GITHUB_API_URL}/repos/test/test", json={"stargazers_count": 0, "forks_count": 0})
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)
    result = service.get_info(repository_name="test/test")

    assert result == GitHupApiResponse(stars=0, forks=0, owner="test", name="test")


def test_get_info_repository_name_invalid(requests_mock):
    requests_mock.get(f"{GITHUB_API_URL}/repos/test/test", json={"stargazers_count": 0, "forks_count": 0})
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)

    with pytest.raises(GitHubServiceRequestException):
        service.get_info(repository_name="lore ipsum")


def test_get_info_github_request_fail_invalid(requests_mock):
    requests_mock.get(f"{GITHUB_API_URL}/repos/test/test", exc=Exception)
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)

    with pytest.raises(GitHubServiceRequestException):
        service.get_info(repository_name="test/test")
