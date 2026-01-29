from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import router
from fastapi.responses import JSONResponse

app = FastAPI(title="Rebel Wireless")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(router)

# Healthcheck endpoint
@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})
