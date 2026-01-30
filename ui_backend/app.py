from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import sys
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    dynamic: bool

@app.post("/analyze")
def analyze_site(data: AnalyzeRequest):
    process = subprocess.run(
        [
            sys.executable,
            "-u",  # 🔑 FORCE UNBUFFERED OUTPUT
            "pipeline/run_pipeline.py",
            data.url,
            str(data.dynamic)
        ],
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, "PYTHONUNBUFFERED": "1"}
    )

    return {
        "output": process.stdout,
        "errors": process.stderr
    }
