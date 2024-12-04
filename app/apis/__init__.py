from fastapi import FastAPI
from . import api


def configure_routes(app: FastAPI):
    app.include_router(api.router)
