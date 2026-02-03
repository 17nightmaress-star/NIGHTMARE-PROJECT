from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/auth/request-otp")
def request_otp():
    return {"requiresPasswordHint": True}


