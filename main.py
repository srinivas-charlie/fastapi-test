from fastapi import FastAPI, Request
from db import engine, Base
import models
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



app = FastAPI()

# Point to templates folder
templates = Jinja2Templates(directory="templates")

@app.get("/")
def homepage():
    return ["name", "srinivas"]


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})


@app.get("/dashboard")
def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})










