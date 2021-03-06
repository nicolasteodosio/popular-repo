import pytest
from config import GITHUB_API_ACCESS_TOKEN, GITHUB_API_URL
from exceptions import (
    GitHubServiceRequestException,
    RepositoryNameException,
    RequestForbiddenException,
    RequestMovedPermanently,
    RequestNotFoundException,
)
from schemas.github import GitHupApiOrgResponse, GitHupApiResponse
from services.github import GitHubService


def test_get_info(requests_mock):
    requests_mock.get(f"{GITHUB_API_URL}/repos/test/test", json={"stargazers_count": 0, "forks_count": 0})
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)
    result = service.get_info(repository_name="test/test")

    assert result == GitHupApiResponse(stars=0, forks=0, owner="test", name="test")


def test_get_info_repository_name_invalid(requests_mock):
    requests_mock.get(f"{GITHUB_API_URL}/repos/test/test", json={"stargazers_count": 0, "forks_count": 0})
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)

    with pytest.raises(RepositoryNameException):
        service.get_info(repository_name="lore ipsum")


@pytest.mark.parametrize(
    "status_code, custom_exception",
    [
        (403, RequestForbiddenException),
        (404, RequestNotFoundException),
        (301, RequestMovedPermanently),
        (500, GitHubServiceRequestException),
    ],
)
def test_get_info_github_request_fail(requests_mock, status_code, custom_exception):

    requests_mock.get(f"{GITHUB_API_URL}/repos/test/test", status_code=status_code)
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)

    with pytest.raises(custom_exception):
        service.get_info(repository_name="test/test")


def test_get_info_github_request_fail_invalid(requests_mock):
    requests_mock.get(f"{GITHUB_API_URL}/repos/test/test", exc=Exception)
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)

    with pytest.raises(GitHubServiceRequestException):
        service.get_info(repository_name="test/test")


def test_get_org_info(requests_mock):
    requests_mock.get(
        f"{GITHUB_API_URL}/orgs/test/repos", json=[{"stargazers_count": 0, "forks_count": 0, "name": "test"}]
    )
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)
    result = service.get_org_info(org_name="test")

    assert result == GitHupApiOrgResponse(items=[GitHupApiResponse(stars=0, forks=0, owner="test", name="test")])


@pytest.mark.parametrize(
    "status_code, custom_exception",
    [
        (403, RequestForbiddenException),
        (404, RequestNotFoundException),
        (301, RequestMovedPermanently),
        (500, GitHubServiceRequestException),
    ],
)
def test_get_org_info_github_request_fail(requests_mock, status_code, custom_exception):

    requests_mock.get(f"{GITHUB_API_URL}/orgs/test/repos", status_code=status_code)
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)

    with pytest.raises(custom_exception):
        service.get_org_info(org_name="test")


def test_get_org_info_github_request_fail_invalid(requests_mock):
    requests_mock.get(f"{GITHUB_API_URL}/orgs/test/repos", exc=Exception)
    service = GitHubService(url=GITHUB_API_URL, access_token=GITHUB_API_ACCESS_TOKEN)

    with pytest.raises(GitHubServiceRequestException):
        service.get_org_info(org_name="test")
