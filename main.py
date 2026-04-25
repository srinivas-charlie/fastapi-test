from fastapi import FastAPI
from db import engine, Base
import models

app = FastAPI()

@app.get("/")
def homepage():
    return ["name", "srinivas"]


@app.get("/root")
def root_page():
    print(app)








