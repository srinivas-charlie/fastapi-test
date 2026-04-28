from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from db import engine
from models import Base


app = FastAPI(debug=True)

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def homepage():
    return ["name", "srinivas"]

@app.get("/dashboard")
def get_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
         context={}
        
        )

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
    request=request, 
    name="login.html", 
    context={} # Add any other variables here
)









