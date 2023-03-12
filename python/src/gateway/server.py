import os, gridfs, pika, json
from fastapi import FastAPI, Request
from pymongo import MongoClient
from gridfs import GridFS
from fastapi import HTTPException
from fastapi import File, UploadFile

from auth import validate
from auth_service import access
from storage import util

app = FastAPI()

client = MongoClient(os.environ["DATABASE_URL"])
db = client.get_default_database()
fs = GridFS(db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@app.post("/login")
def login():
    token,error = access.login(Request)
    if not error:
        return token
    else:
        return error

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    _access, error = validate.token(request)
    access = json.loads(_access)
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required",400

        for _,file in request.files.items():
            error = util.upload(file, fs, channel, access)

            if error:
                return error
        
        return "success!", 200
    
    else:
        return "not authorized", 401


@app.get("/download/")
def download():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)