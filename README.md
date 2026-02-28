# Financial Document Analyzer

## Overview

This project is an AI-powered system designed to analyze financial documents such as corporate earnings reports, investor updates, and financial disclosures.

The system extracts structured insights including:

* Financial health indicators
* Investment signals
* Risk factors

The repository provided for this assignment was intentionally unstable and incomplete.
The primary goal was not only to fix visible errors, but to stabilize the system at an architectural level so that it could operate reliably under realistic workloads.

---

# Engineering Approach

Instead of debugging through trial and error, the following structured method was used:

### XYZ Debug Framework

For each failure:

* **Found X** → Identified the root cause
* **Used Y** → Applied an engineering solution
* **Got Z** → Achieved measurable system stability

This ensured long-term correctness rather than temporary fixes.

---

# Bugs Found & Fixes

## 1. AI Tool Integration Failure

### Found

The financial document reader was implemented as a raw function, while CrewAI expects tools to follow a structured interface.

This caused:

* Runtime validation errors
* Task initialization failures

### Used

Refactored the reader into a CrewAI-compatible `BaseTool`:

* Introduced proper abstraction
* Ensured tool-agent compatibility
* Aligned with CrewAI execution lifecycle

### Got

Agents successfully accessed PDF data without runtime crashes.

---

## 2. LLM Dependency Instability

### Found

The original implementation depended on OpenAI without proper configuration.

This resulted in:

* API key errors
* Model compatibility issues
* Execution failures

### Used

Migrated the AI layer to Google Gemini:

* Integrated via CrewAI’s LLM abstraction
* Ensured compatibility with tool execution
* Stabilized environment configuration

### Got

Reliable AI execution without credential dependency issues.

---

## 3. Blocking Execution Model

### Found

Financial analysis was executed synchronously inside FastAPI.

Impact:

* Long-running AI tasks blocked API responses
* System could process only one document at a time
* Risk of timeouts

### Used

Re-architected execution using:

* Redis for task queuing
* Celery for background workers

Execution moved from:

User → API → AI → Response

to:

User → API → Redis Queue → Celery Worker → AI → Result

### Got

* Non-blocking API
* Concurrent document processing
* Improved scalability

---

## 4. Task Execution Failure

### Found

Celery workers started successfully but ignored queued tasks.

Cause:

* Tasks were not registered during worker boot

### Used

* Explicit task registration
* Avoided reliance on autodiscovery

### Got

Background processing executed consistently across worker instances.

---

## 5. Environment Loading Crash

### Found

Celery workers crashed during startup due to UTF-8 decoding errors.

Investigation revealed:

CrewAI internally invoked dotenv loading, which scanned the entire project directory.

Uploaded PDF files were mistakenly interpreted as environment files.

Since PDFs are binary, this caused decoding failures.

### Used

* Restricted dotenv to load only `.env`
* Prevented directory-wide scanning

### Got

Worker initialization became stable and predictable.

---

## 6. Distributed File Access Issue

### Found

Background workers intermittently failed to access uploaded documents.

Reason:

Celery operates in a separate execution context.

Relative file paths used by FastAPI were not valid inside worker processes.

### Used

Converted uploaded document paths to absolute paths.

### Got

Consistent file access across:

* API layer
* Worker layer

---

# Final Architecture

The system evolved from a tightly coupled prototype to a distributed processing model.

### Initial Flow

User → API → AI → Response

### Final Flow

User → API → Redis Queue → Celery Worker → AI Processing → Result Retrieval

This enables:

* Parallel processing
* High-latency AI workloads
* Fault isolation

---

# Setup Instructions

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Start Redis

```bash
docker run -d -p 6379:6379 redis
```

---

## 3. Configure Environment

Create `.env`

```
GOOGLE_API_KEY=your_api_key_here
```

---

## 4. Start Celery Worker

```
celery -A celery_worker.celery_app worker --loglevel=info
```

---

## 5. Start API Server

```
uvicorn main:app --reload
```

---

# Usage

Upload financial documents such as:

* Earnings reports
* Investor presentations
* Corporate filings

---

# API Documentation

## Health Check

GET /

Returns:

```
Financial Document Analyzer API is running
```

---

## Analyze Document

POST /analyze

Upload a financial PDF.

Request:

* file: PDF
* query: Optional analysis instruction

Response:

```
{
  "status": "processing",
  "task_id": "xyz"
}
```

---

## Check Status

GET /status/{task_id}

Returns:

```
{
  "task_id": "xyz",
  "status": "SUCCESS",
  "result": "Analysis Output"
}
```

---

# Technologies Used

* FastAPI – API Layer
* CrewAI – Agent Orchestration
* Google Gemini – AI Analysis
* Redis – Task Queue
* Celery – Background Execution

---

# Outcome

The system now supports:

* Concurrent document analysis
* Stable AI execution
* Non-blocking API responses
* Scalable processing

---

# Conclusion

This assignment evolved from debugging broken functionality into designing a resilient AI processing pipeline.

By identifying systemic failures rather than patching symptoms, the project now reflects real-world execution patterns used in scalable AI systems.
