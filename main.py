from fastapi import FastAPI
from models import base
from database import engine
from routers import authentication,parts,suppliers
app=FastAPI()

base.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(parts.router)
app.include_router(suppliers.router)


@app.get('/')
def main_page():
    return {"message":"Hello"}






