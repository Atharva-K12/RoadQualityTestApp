from pydantic import BaseModel
# from fastapi import FastAPI, File, UploadFile
class InputSchema(BaseModel):
    filename : str
    
# class emailAddrSchema(BaseModel):
    # emailIdList :list[str]