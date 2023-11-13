from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

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
