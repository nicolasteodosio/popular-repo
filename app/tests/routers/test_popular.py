import pytest
from exceptions import (
    CalculateScoreException,
    GitHubServiceRequestException,
    RepositoryForbiddenException,
    RepositoryMovedPermanently,
    RepositoryNameException,
    RepositoryNotFoundException,
)
from routers.popular import PopularView
from schemas.github import GitHupApiResponse
from schemas.popular import PopularResponseModel
from services.github import GitHubService
from services.popular import PopularService


def test_check(mocker):
    mocked_git_service = mocker.Mock(autospec=GitHubService)
    mocked_popular_service = mocker.Mock(autospec=PopularService)

    view = PopularView(github_service=mocked_git_service, popular_service=mocked_popular_service)

    mocked_git_service.get_info.return_value = GitHupApiResponse(stars=5, name="test", forks=9, owner="lore")
    mocked_popular_service.calculate_score.return_value = PopularResponseModel(
        score=5, owner="lore", name="test", is_popular=False
    )

    response = view.check(repository_name="test")

    assert response.status_code == 200
    mocked_git_service.get_info.assert_called_once()
    mocked_popular_service.calculate_score.assert_called_once()


@pytest.mark.parametrize(
    "custom_exception, status_code",
    [
        (RepositoryNotFoundException, 404),
        (RepositoryNameException, 500),
        (RepositoryForbiddenException, 500),
        (RepositoryMovedPermanently, 500),
        (GitHubServiceRequestException, 500),
    ],
)
def test_check_github_service_exceptions(mocker, custom_exception, status_code):
    mocked_git_service = mocker.Mock(autospec=GitHubService)
    mocked_popular_service = mocker.Mock(autospec=PopularService)

    view = PopularView(github_service=mocked_git_service, popular_service=mocked_popular_service)

    mocked_git_service.get_info.side_effect = custom_exception
    mocked_popular_service.calculate_score.return_value = PopularResponseModel(
        score=5, owner="lore", name="test", is_popular=False
    )

    response = view.check(repository_name="test")

    assert response.status_code == status_code
    mocked_git_service.get_info.assert_called_once()
    mocked_popular_service.calculate_score.assert_not_called()


def test_check_popular_service_exceptions(mocker):
    mocked_git_service = mocker.Mock(autospec=GitHubService)
    mocked_popular_service = mocker.Mock(autospec=PopularService)

    view = PopularView(github_service=mocked_git_service, popular_service=mocked_popular_service)

    mocked_git_service.get_info.return_value = GitHupApiResponse(stars=5, name="test", forks=9, owner="lore")
    mocked_popular_service.calculate_score.side_effect = CalculateScoreException

    response = view.check(repository_name="test")

    assert response.status_code == 500
    mocked_git_service.get_info.assert_called_once()
    mocked_popular_service.calculate_score.assert_called_once()
