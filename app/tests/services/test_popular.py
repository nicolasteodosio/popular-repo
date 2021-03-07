import pytest
from schemas.github import GitHupApiResponse
from schemas.popular import PopularResponseModel
from services.popular import PopularService


def test_calculate_score_is_popular_false():
    service = PopularService()
    data = GitHupApiResponse(stars=0, forks=0, owner="test", name="test")
    result = service.calculate_score(repository_data=data)

    assert result == PopularResponseModel(owner="test", score=0, name="test", is_popular=False)


def test_calculate_score_is_popular_true():
    service = PopularService()
    data = GitHupApiResponse(stars=500, forks=50, owner="test", name="test")
    result = service.calculate_score(repository_data=data)

    assert result == PopularResponseModel(owner="test", score=600, name="test", is_popular=True)


def test_calculate_score_exception():
    service = PopularService()

    with pytest.raises(Exception):
        service.calculate_score(repository_data={})
