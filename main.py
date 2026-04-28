from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from db import engine, get_db
from models import Base, User
from sqlalchemy.orm import Session


app = FastAPI(debug=True)

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")



@app.get("/dashboard")
def get_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
         context={}
        
        )

@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse(
    request=request, 
    name="login.html", 
    context={} # Add any other variables here

    )

@app.post("/")
def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db:Session = Depends(get_db)
    ):

    user = db.query(User).filter(User.email == email).first()

    if not user or user.password != password:
       raise HTTPException(status_code=401, detail="Invalid email or password")

    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="register.html", 
        context={}
    )

@app.post("/register")
def create_user(
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
 new_user = User(name=name, email=email, password=password)

 db.add(new_user)
 db.commit()
 db.refresh(new_user)

 return RedirectResponse(url="/", status_code=303)
