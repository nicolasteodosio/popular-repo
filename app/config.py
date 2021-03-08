import os

GITHUB_API_ACCESS_TOKEN = os.getenv("GITHUB_API_ACCESS_TOKEN")
GITHUB_API_URL = os.getenv("GITHUB_API_URL")

STAR_MULTIPLIER = int(os.getenv("STAR_MULTIPLIER", 1))
FORK_MULTIPLIER = int(os.getenv("FORK_MULTIPLIER", 2))
POPULAR_THRESHOLD = int(os.getenv("POPULAR_THRESHOLD", 500))

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_KEY_TTL = int(os.getenv("REDIS_KEY_TTL", 600))
