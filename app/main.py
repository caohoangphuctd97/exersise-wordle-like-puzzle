from fastapi import FastAPI
from app.apis import configure_routes

app = FastAPI(
    title="Wordle-like puzzle",
    version="0.0.1"
)

configure_routes(app)
