from fastapi import FastAPI
import jwt, datetime, os
import models
from config import engine
import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router.router,prefix = "/user", tags =["user"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
    


