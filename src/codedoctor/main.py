from fastapi import FastAPI

from codedoctor.api.routes import router


app = FastAPI(
    title="CodeDoctor API",
    version="0.1.0",
)

app.include_router(
    router,
    prefix="/api/v1",
)