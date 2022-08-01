from fastapi import FastAPI, File, UploadFile
import shutil

app=FastAPI()

@app.get("/")
def landingPage(): return {"message": "Hello World"}


@app.post("/InputVideo")
def inputVideo(file : UploadFile): 
    
    with open("test.mp4","wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename}