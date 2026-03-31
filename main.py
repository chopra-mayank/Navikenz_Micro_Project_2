from fastapi import FastAPI
import models
from database import engine
from auth import router as auth_router
from transactions import router as txn_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(txn_router)

@app.get("/")
def home():
    return {"message": "Finance API running 🚀"}