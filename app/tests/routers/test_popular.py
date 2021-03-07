from routers.popular import PopularView
from schemas.github import GitHupApiResponse
from schemas.popular import PopularResponseModel
from services.github import GitHubService
from services.popular import PopularService


def test_create_order(mocker):
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
