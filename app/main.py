import uvicorn
from fastapi import FastAPI
from app.models import Base
from app.config import engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task API",
    description="A simple API to manage tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url='/redoc',
    openapi_url="/api/openapi.json",

)
app.include_router(router, prefix='/api', tags=['tasks'])


@app.get("/")
def root():
    return {"message": "API is running ✅!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)