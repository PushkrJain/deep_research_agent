from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict, Any
import logging
import os

class DraftAgent:
    def __init__(self, model="gemini-1.5-pro-latest", temperature=0.7):
        self.logger = logging.getLogger(__name__)
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Enhanced prompt to handle query variations
        self.prompt = ChatPromptTemplate.from_template(
            """Create a comprehensive research report based on these inputs:
            
            Original Research Question: {query}
            
            Research Data:
            {results}
            
            Structure your report with:
            1. Executive Summary (include note about any query variations)
            2. Key Findings (bullet points)
            3. Detailed Analysis
            4. Conclusion
            5. Sources
            
            Note any query variations in the Executive Summary if applicable.
            Use markdown formatting and cite sources as [Source 1], [Source 2], etc."""
        )
        
        self.chain = (
            {"query": RunnablePassthrough(), "results": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    async def generate_report(self, query: str, research_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a research report with query variation notes"""
        try:
            self.logger.info("Generating research report")
            
            if not research_results:
                raise ValueError("No research data provided")
            
            # Check for query variations
            query_variations = set(r['query_used'] for r in research_results if 'query_used' in r)
            
            # Generate full report
            report = await self.chain.ainvoke({
                "query": query,
                "results": research_results
            })
            
            return {
                "question": query,
                "answer": report,
                "sources": self._process_sources(research_results),
                "query_variations": list(query_variations)
            }
        except Exception as e:
            self.logger.error(f"Report generation failed: {str(e)}", exc_info=True)
            return {
                "question": query,
                "answer": f"Error generating report: {str(e)}",
                "sources": [],
                "query_variations": []
            }

    def _process_sources(self, research_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format source information with query info"""
        return [
            {
                "id": i+1,
                "url": res.get('url', ''),
                "title": res.get('title', f'Source {i+1}'),
                "score": res.get('score', 0.0),
                "query_used": res.get('query_used', 'original')
            }
            for i, res in enumerate(research_results)
            if res.get('url')
        ]
