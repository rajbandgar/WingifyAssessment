## Importing libraries and files
import os
from dotenv import load_dotenv


from crewai import Agent, LLM
from tools import FinancialDocumentTool

# -----------------------------
# Gemini LLM Configuration
# -----------------------------
llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3   # Lower for factual analysis
)

# -----------------------------
# Tool Instance
# -----------------------------
financial_doc_tool = FinancialDocumentTool()

# -----------------------------
# Financial Analyst Agent
# -----------------------------
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents and provide accurate, data-driven investment insights based on real financial metrics: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with expertise in corporate financial statements, earnings reports, "
        "and macroeconomic indicators. You evaluate revenue growth, profitability, liquidity, leverage, and risk exposure. "
        "Your insights are grounded in factual financial data and realistic market understanding."
    ),
    tools=[financial_doc_tool],
    llm=llm,
    max_iter=2,
    max_rpm=5,
    allow_delegation=False
)

# -----------------------------
# Document Verifier Agent
# -----------------------------
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether the uploaded file is a valid financial document and ensure relevant financial content exists.",
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in identifying financial disclosures, earnings data, balance sheet elements, and operational metrics. "
        "You ensure that analysis is performed only on relevant financial information."
    ),
    tools=[financial_doc_tool],
    llm=llm,
    max_iter=1,
    max_rpm=3,
    allow_delegation=False
)

# -----------------------------
# Investment Advisor Agent
# -----------------------------
investment_advisor = Agent(
    role="Investment Strategist",
    goal="Provide balanced investment recommendations based on financial health and market outlook.",
    verbose=True,
    backstory=(
        "You analyze company fundamentals to suggest realistic investment strategies. "
        "You consider growth prospects, risk exposure, competitive positioning, and macro trends."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=3,
    allow_delegation=False
)

# -----------------------------
# Risk Assessment Agent
# -----------------------------
risk_assessor = Agent(
    role="Risk Analyst",
    goal="Identify financial and market risks present in the analyzed document.",
    verbose=True,
    backstory=(
        "You evaluate operational risk, market volatility, leverage exposure, and industry threats. "
        "Your focus is realistic downside scenarios and financial sustainability."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=3,
    allow_delegation=False
)