import logging

from config import FORK_MULTIPLIER, POPULAR_THRESHOLD, STAR_MULTIPLIER
from exceptions import CalculateScoreException
from schemas.github import GitHupApiResponse
from schemas.popular import PopularResponseModel

logger = logging.getLogger(__name__)


class PopularService:
    def __init__(self):
        self.star_multiplier = STAR_MULTIPLIER
        self.fork_multiplier = FORK_MULTIPLIER
        self.popular_threshold = POPULAR_THRESHOLD

    def calculate_score(self, repository_data: GitHupApiResponse) -> PopularResponseModel:
        try:
            score = repository_data.stars * self.star_multiplier + repository_data.forks * self.fork_multiplier
            is_popular = score >= self.popular_threshold

            return PopularResponseModel(
                owner=repository_data.owner, score=score, name=repository_data.name, is_popular=is_popular
            )
        except Exception as ex:
            logger.error(f"Error calculating score ex: {ex}")
            raise CalculateScoreException(ex)
