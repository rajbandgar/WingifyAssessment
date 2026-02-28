from celery_worker import celery_app
from crew_runner import run_crew

@celery_app.task(name="tasks.process_financial_analysis")
def process_financial_analysis(query, file_path):
    result = run_crew(query, file_path)
    return str(result)