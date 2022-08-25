from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import base64

from Schemas import InputSchema ,emailAddrSchema

from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from fpdf import FPDF


app=FastAPI()
global cwdPath

# pwdPath="./SavedDirectoryResults"
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cwdPath = ".\SavedDirectoryResults"

@app.get("/")
def landingPage(): return {"message": "Hello World"}

@app.post("/MakeDirectory")
def makeDirectory(dirName: str):
    global cwdPath
    cwdPath =".\SavedDirectoryResults"
    cwdPath = os.path.join(cwdPath,dirName)
    try:
        os.mkdir(cwdPath)
        print(cwdPath)
    except OSError:
        return{"message":"Directory already exists"}
    return {"message":"Directory created"}

@app.post("/InputVideo")
async def inputVideo(file : UploadFile): 
    
    filename1 = os.path.join(cwdPath, "InputVideo.mp4")
    with open(filename1,"wb") as BufferWriter:
        shutil.copyfileobj(file.file, BufferWriter)
    return {"message":"Video uploaded"}

@app.post("/InputGPRData")
def inputGPRData(file : UploadFile):
    global fnameGPR
    fnameGPR = file.filename
    # cwdPath = "./SavedDirectoryResults"
    filename2 = os.path.join(cwdPath, "InputGPR.csv")
    with open(filename2,"wb") as BufferWriter:
        shutil.copyfileobj(file.file, BufferWriter)
    return {"message":"File uploaded"}


def GeneratePdf():    
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size = 15)

    pdf.cell(200, 10, txt = "GeeksforGeeks",
		ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "A Computer Science portal for geeks.",
		ln = 2, align = 'C')
    # print(cwdPath)
    
    reportPath = os.path.join(cwdPath, "Report.pdf")
    pdf.output(reportPath,"F")
    # filename1 = os.path.join(cwdPath, "Report.pdf")
    # with open(filename1,"wb") as BufferWriter:
    #     shutil.copyfileobj(pdf, BufferWriter)
    return 1
    
@app.post("/executeScript")
def executeScript(): 
    
    # input to model wrapper func()\
    # output from model wrapper func()
    x = GeneratePdf()
    #save output data into SavedDirectoryResults
    if(x==1):
        return{"message":"Script executed , output data saved"}
    return{"message":"Script execution failed"}

@app.post("/sendEmail")
def sendEmail(emailAddr : emailAddrSchema ):
    import smtplib, ssl
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "adeshpande@students.vnit.ac.in"
    password ="Adw@it1191"
    receiver_email = "dadwait51@gmail.com"
    
    # OpVideofile =cwdPath +".\Output\OutputVideo.mp4"
    # OpReportFile = cwdPath +".\Output\OutputReport.pdf"
    OpVideofile = os.path.join(cwdPath, "InputVideo.mp4")
    OpReportFile = os.path.join(cwdPath, "Report.pdf")
    
    files=[]
    files.append(OpVideofile)
    files.append(OpReportFile)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Road Quality Test Report"

    msg.attach(MIMEText(" body text"))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        msg.attach(part)
        
        
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo() 
        server.starttls(context=context)
        server.ehlo() 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
            
    return{"message":"Email sent"} 

@app.get("/getVideo")
def getVideo():
    newOutputVideoPath = os.path.join(cwdPath,"InputVideo.mp4")
    return FileResponse(newOutputVideoPath)

@app.get("/getReport")
def getReport():
    newOutputReportPath = os.path.join(cwdPath,"Report.pdf")
    return FileResponse(newOutputReportPath)

@app.get("/getOutputCoordinates")
def getOutputCoordinates():
    newOutputCoordinatesPath = os.path.join(cwdPath,"InputGPR.csv")
    return FileResponse(newOutputCoordinatesPath)
