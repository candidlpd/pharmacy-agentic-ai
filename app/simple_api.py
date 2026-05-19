from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Eli Lilly Pharmacy AI")

class CaseRequest(BaseModel):
    drug: str
    dose: str
    indication: str

@app.get("/")
def root():
    return {"status": "running", "message": "Eli Lilly Pharmacy AI API"}

@app.post("/process")
def process_case(request: CaseRequest):
    return {
        "status": "processed",
        "drug": request.drug,
        "approved": True,
        "message": f"Processed {request.drug} for {request.indication}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)