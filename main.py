from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import settings

# DB

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# MODELS

Base = declarative_base()




app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    with open("public/index.html") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/test/{test}")
async def testing(test: int):
    return {"test": test}
