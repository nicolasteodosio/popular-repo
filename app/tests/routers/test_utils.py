from routers.utils import UtilsView


def test_healthcheck():
    view = UtilsView()

    response = view.health_check()

    assert response.status_code == 200
