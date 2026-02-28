import os
import sys
from celery import Celery
from dotenv import load_dotenv

# Load ONLY .env explicitly
load_dotenv(dotenv_path=".env")

# Add project root to path
sys.path.append(os.getcwd())

celery_app = Celery(
    "financial_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Import tasks AFTER env load
import tasks

celery_app.conf.update(
    task_track_started=True,
    result_expires=3600
)