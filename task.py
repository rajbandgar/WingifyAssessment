## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier
from tools import FinancialDocumentTool

financial_doc_tool = FinancialDocumentTool()

# -----------------------------
# Document Verification Task
# -----------------------------
verification = Task(
    description="""
Verify whether the uploaded document at {file_path} is a financial report.

Check for:
- Financial statements
- Revenue data
- Profitability indicators
- Market disclosures

Confirm whether meaningful financial data exists for analysis.
""",
    expected_output="""
State whether the document is a valid financial document suitable for analysis.
""",
    agent=verifier,
    tools=[financial_doc_tool],
    async_execution=False,
)

# -----------------------------
# Financial Analysis Task
# -----------------------------
analyze_financial_document = Task(
    description="""
Analyze the financial document located at {file_path}.

Provide:

1. Company financial summary
2. Revenue and profitability insights
3. Balance sheet strength
4. Cash flow outlook
5. Growth indicators

Answer the user's query: {query}
""",
    expected_output="""
Provide a structured financial analysis including:
- Key financial highlights
- Trends observed
- Business performance insights
""",
    agent=financial_analyst,
    tools=[financial_doc_tool],
    async_execution=False,
)

# -----------------------------
# Investment Analysis Task
# -----------------------------
investment_analysis = Task(
    description="""
Based on the analyzed financial data from {file_path}, evaluate investment attractiveness.

Consider:
- Financial health
- Growth potential
- Market positioning
- Profitability trends

Provide realistic investment outlook.
""",
    expected_output="""
Provide:
- Investment strengths
- Weaknesses
- Long-term outlook
- Buy / Hold / Watch perspective
""",
    agent=financial_analyst,
    tools=[financial_doc_tool],
    async_execution=False,
)

# -----------------------------
# Risk Assessment Task
# -----------------------------
risk_assessment = Task(
    description="""
Assess risks present in the financial document at {file_path}.

Evaluate:
- Financial leverage
- Market exposure
- Operational risks
- Industry threats
""",
    expected_output="""
Provide realistic risk analysis including:
- Financial risks
- Market risks
- Strategic risks
""",
    agent=financial_analyst,
    tools=[financial_doc_tool],
    async_execution=False,
)