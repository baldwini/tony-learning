from typing import Annotated
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

#Good for small files as it's all stored in memory
@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File(description="A file read as bytes")] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

#Good for large files as it uses spooled file that
#stores up to a max in memory, then goes to disk
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"Message": "No upload file sent"}
    else:
        return {"filename": file.filename}

#Use File to attach additional metadata into UploadFile
@app.post("/uploadfiles/")
async def create_upload_file(
        file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}