
from crewai_tools import SerperDevTool, PDFSearchTool
from crewai.tools import BaseTool

from crewai import LLM
import os


gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

## Creating search tool
search_tool = SerperDevTool()

## Creating custom Financial Document Tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads and extracts insights from uploaded financial PDF documents"

    def _run(self, query: str = "", file_path: str = "data/sample.pdf"):
        """
        Extract and analyze content from uploaded financial PDF
        """

        try:
            # Use uploaded file instead of hardcoded sample
            pdf_tool = PDFSearchTool(
    pdf=file_path,
    llm=gemini_llm
)

            result = pdf_tool.run(
                query if query else "Provide a financial summary of this document"
            )

            return result

        except Exception as e:
            return f"Error processing financial document: {str(e)}"