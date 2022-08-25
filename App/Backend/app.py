from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
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



app=FastAPI()

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

cwdPath = ".\SavedDirectoryResults\Trash"

@app.get("/")
def landingPage(): return {"message": "Hello World"}


@app.post("/InputVideo")
def inputVideo(file : UploadFile): 
    
    # with open("test.mp4","wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    os.path.join(cwdPath,file.filename)
    return {"filename": file.filename}

@app.post("/InputGPRData")
def inputGPRData(file : UploadFile):
    os.path.join(cwdPath,file.filename)
    return {"filename": file.filename}


@app.post("/MakeDirectory")
def makeDirectory(dirName: str ,inputData:InputSchema):
    
    cwdPath =".\SavedDirectoryResults"
    cwdPath = os.path.join(cwdPath,dirName)
    try:
        os.mkdir(cwdPath)
        print(cwdPath)
    except OSError:
        return{"message":"Directory already exists"}
    return {"message":"Directory created","path":inputData.filename}


@app.post("/executeScript")
def executeScript(): 
    
    # input to model wrapper func()\
    # output from model wrapper func()
    
    #save output data into SavedDirectoryResults
    return{"message":"Script executed , output data saved"}



@app.post("/sendEmail")
def sendEmail(emailAddr : emailAddrSchema ):
    import smtplib, ssl
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "adeshpande@students.vnit.ac.in"
    password ="Adw@it1191"
    receiver_email = "dadwait51@gmail.com"
    
    # for email in emailAddr.emailIdList:

        
    #     print(receiver_email)
    # #     message ="""From: adeshpande@students.vnit.ac.in
    # #                 To: xyz@gmail.com
    # #                 Subject: Send mail from python!!

    # # """
    # #     body = "Hi guys,\nThis is a test email.\n Thank you."
    # #     message += body
    file = "./SavedDirectoryResults/0.txt"
    #     fo = open(file, "rb")
    #     filecontent = fo.read()
    #     encodedcontent = base64.b64encode(filecontent)  # base64
    #     # encodedcontent = file

    #     # sender = 'adeshpande@students.vnit.ac.in'
    #     # reciever = 'dadwait51@gmail.com'

    #     marker = "AUNIQUEMARKER"

    #     body ="""
    #     This is a test email to send an attachement.
    #     """
    #     # Define the main headers.
    #     part1 = """From: From Person <adeshpande@students.vnit.ac.in>
    #     To: To Person <dadwait51@gmail.com>
    #     Subject: Sending Attachement
    #     MIME-Version: 1.0
    #     Content-Type: multipart/mixed; boundary=%s
    #     --%s
    #     """ % (marker, marker)

    #     # Define the message action
    #     part2 = """Content-Type: text/plain
    #     Content-Transfer-Encoding:8bit

    #     %s
    #     --%s
    #     """ % (body,marker)

    #     # Define the attachment section
    #     part3 = """Content-Type: multipart/mixed; name=\"%s\"
    #     Content-Transfer-Encoding:base64
    #     Content-Disposition: attachment; filename=%s

    #     %s
    #     --%s--
    #     """ %(file, file, encodedcontent, marker)
    #     message = part1 + part2 + part3
    
   

    files=[]
    files.append(file)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = COMMASPACE.join(receiver_email)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "subject test"

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


