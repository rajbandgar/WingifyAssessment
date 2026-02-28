from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

from tasks import process_financial_analysis
from celery_worker import celery_app

app = FastAPI(title="Financial Document Analyzer")

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

# -----------------------------
# Analyze Endpoint
# -----------------------------
@app.post("/analyze")
async def analyze_financial_document_api(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    file_id = str(uuid.uuid4())
    file_path = os.path.abspath(f"data/financial_document_{file_id}.pdf")

    try:
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if not query:
            query = "Analyze this financial document for investment insights"

        # Send task to Celery
        task = process_financial_analysis.delay(query.strip(), file_path)

        return {
            "status": "processing",
            "task_id": task.id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Task Status Endpoint
# -----------------------------
@app.get("/status/{task_id}")
def get_status(task_id: str):
    task = celery_app.AsyncResult(task_id)

    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None
    }

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)