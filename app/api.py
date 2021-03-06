import uvicorn
from fastapi import FastAPI
from nicelog import setup_logging
from routers.utils import UtilsView

API_VERSION = "v1"


def create_app():
    setup_logging()

    app = FastAPI()
    app.router.redirect_slashes = True

    configure_routers(app)

    return app


def configure_routers(app):
    app.include_router(UtilsView().get_router(), prefix=f"/{API_VERSION}/utils", tags=["utils"], dependencies=[])


if __name__ == "__main__":
    application = create_app()
    uvicorn.run(application, host="0.0.0.0", port=8000)
