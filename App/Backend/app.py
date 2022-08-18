from fastapi import FastAPI, File, UploadFile
import shutil
import os

from Schemas import InputSchema,emailAddrSchema
app=FastAPI()

cwdPath = "D:\Sandisk Docs\VNIT ACAD\sih\RoadQualityTestApp\App\Backend\SavedDirectoryResults\Trash"

@app.get("/")
def landingPage(): return {"message": "Hello World"}


@app.post("/InputVideo")
def inputVideo(file : UploadFile): 
    
    # with open("test.mp4","wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    os.path.join(cwdPath,file.filename)
    return {"filename": file.filename}


@app.post("/MakeDirectory")
def makeDirectory(dirName: str ,inputData:InputSchema):
    
    cwdPath ="D:\Sandisk Docs\VNIT ACAD\sih\RoadQualityTestApp\App\Backend\SavedDirectoryResults"
    cwdPath = os.path.join(cwdPath,dirName)
    try:
        os.mkdir(cwdPath)
    except OSError:
        return{"message":"Directory already exists"}
    return {"message":"Directory created","path":inputData.filename}


@app.post("/executeScript")
def executeScript(): 
    
    # input to model wrapper func()\
    # output from model wrapper func()
    
    #save output data into SavedDirectoryResults
    return{"message":"Script executed , output data saved"}



@app.post("/sendEmail") #has error
def sendEmail(emailAddr : emailAddrSchema):
    import smtplib, ssl
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "dadwait51@gmail.com"
    for email in emailAddr.emailIdList:
        
        receiver_email = email
        password ="Meghshy@m29"
        message = """\
        Subject: Hi there
        Im sending an email through python code."""
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo() 
            server.starttls(context=context)
            server.ehlo() 
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            
    return{"message":"Email sent"} 


