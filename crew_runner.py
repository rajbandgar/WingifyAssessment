from crewai import Crew, Process


from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import verification, analyze_financial_document, investment_analysis, risk_assessment

def run_crew(query: str, file_path: str):
    financial_crew = Crew(
        agents=[
            verifier,
            financial_analyst,
            investment_advisor,
            risk_assessor
        ],
        tasks=[
            verification,
            analyze_financial_document,
            investment_analysis,
            risk_assessment
        ],
        process=Process.sequential
    )

    return financial_crew.kickoff({
        "query": query,
        "file_path": file_path
    })