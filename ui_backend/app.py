from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# IMPORT YOUR PIPELINE FUNCTION
from pipeline.run_pipeline import run_pipeline  # we’ll define this next

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    dynamic: bool = True


@app.post("/analyze")
def analyze_site(data: AnalyzeRequest):
    result = run_pipeline(
        url=data.url,
        use_dynamic=data.dynamic
    )
    return result
