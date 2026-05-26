from fastapi import (
    FastAPI,
    Request,
    Depends,
    Form,
    HTTPException,
    UploadFile,
    File
)

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.orm import Session

from db import engine, get_db
from models import Base, User

import base64


app = FastAPI(debug=True)


# ======================================
# SESSION MIDDLEWARE
# ======================================
app.add_middleware(
    SessionMiddleware,
    secret_key="THIS_IS_MY_SECRET_KEY"
)


# ======================================
# CREATE TABLES
# ======================================
Base.metadata.create_all(bind=engine)


# ======================================
# JINJA TEMPLATES
# ======================================
templates = Jinja2Templates(
    directory="templates"
)


# ======================================
# LOGIN PAGE
# ======================================
@app.get("/")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )


# ======================================
# LOGIN USER
# ======================================
@app.post("/")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or user.password != password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    request.session["user"] = user.email

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# ======================================
# DASHBOARD
# ======================================
@app.get("/dashboard")
def get_dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    session_user = request.session.get("user")

    if not session_user:

        return RedirectResponse(
            url="/"
        )

    current_user = db.query(User).filter(
        User.email == session_user
    ).first()

    if not current_user:

        return RedirectResponse(
            url="/"
        )

    photo_base64 = None

    if current_user.profile_photo:

        photo_base64 = base64.b64encode(
            current_user.profile_photo
        ).decode("utf-8")

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": current_user,
            "role": current_user.role,
            "profile_photo": photo_base64
        }
    )


# ======================================
# REGISTER PAGE
# ======================================
@app.get("/register")
def register_page(
    request: Request,
    db: Session = Depends(get_db)
):

    session_user = request.session.get("user")

    if not session_user:

        return RedirectResponse(
            url="/"
        )

    current_user = db.query(User).filter(
        User.email == session_user
    ).first()

    if not current_user:

        return RedirectResponse(
            url="/"
        )

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )


# ======================================
# CREATE USER
# ======================================
@app.post("/register")
def create_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    session_user = request.session.get("user")

    if not session_user:

        return RedirectResponse(
            url="/"
        )

    current_user = db.query(User).filter(
        User.email == session_user
    ).first()

    if not current_user:

        return RedirectResponse(
            url="/"
        )

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only admin can create users"
        )

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    photo_data = profile_photo.file.read()

    new_user = User(
        name=name,
        email=email,
        password=password,
        role="user",
        profile_photo=photo_data
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# ======================================
# LOGOUT
# ======================================
@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )


# ======================================
# USERS LIST
# ======================================
@app.get("/users")
def users_list(
    request: Request,
    db: Session = Depends(get_db)
):

    session_user = request.session.get("user")

    if not session_user:

        return RedirectResponse(
            url="/"
        )

    current_user = db.query(User).filter(
        User.email == session_user
    ).first()

    if not current_user:

        return RedirectResponse(
            url="/"
        )

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    users = db.query(User).all()

    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "request": request,
            "users": users,
            "current_user": current_user
        }
    )