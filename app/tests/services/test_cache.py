import redis
from config import REDIS_KEY_TTL
from services.cache import CacheService


def test_set_key(mocker):
    mock_connection = mocker.Mock(autospec=redis.Redis)
    service = CacheService(connection=mock_connection)

    service.set_key(key="test", value={"test": "test"})

    mock_connection.set.assert_called_once_with("test", '{"test": "test"}', ex=REDIS_KEY_TTL)


def test_check_none(mocker):
    mock_connection = mocker.Mock(autospec=redis.Redis)
    service = CacheService(connection=mock_connection)

    mock_connection.get.return_value = None
    response = service.check(key="test")

    assert response is None
    mock_connection.get.assert_called_once_with("test")


def test_check(mocker):
    mock_connection = mocker.Mock(autospec=redis.Redis)
    service = CacheService(connection=mock_connection)

    mock_connection.get.return_value = b"{'test': 'test'}"
    response = service.check(key="test")

    assert response == "{'test': 'test'}"
    mock_connection.get.assert_called_once_with("test")
