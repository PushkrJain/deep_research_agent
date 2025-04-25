import os
from tavily import TavilyClient
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import logging

class ResearchAgent:
    def __init__(self, model="gemini-1.5-pro-latest", temperature=0.7):
        self.logger = logging.getLogger(__name__)
        
        # Verify API keys
        if not os.getenv("TAVILY_API_KEY"):
            raise ValueError("TAVILY_API_KEY environment variable not set")
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        @tool
        def web_search(query: str, is_retry: bool = False) -> List[Dict[str, Any]]:
            """Perform comprehensive web search using Tavily API"""
            try:
                self.logger.info(f"Executing {'retry ' if is_retry else ''}search for: {query}")
                response = self.tavily.search(
                    query=query,
                    search_depth="advanced",
                    include_raw_content=True,
                    max_results=5,
                    include_answer=True
                )
                
                # Structure results
                structured_results = []
                for item in response.get('results', []):
                    structured_results.append({
                        "content": item.get('content', ''),
                        "url": item.get('url', ''),
                        "title": item.get('title', 'No title')[:100],
                        "score": float(item.get('score', 0.0)),
                        "query_used": query
                    })
                
                # Include direct answer if available
                if response.get('answer'):
                    structured_results.append({
                        "content": response['answer'],
                        "url": "",
                        "title": "Direct Answer",
                        "score": 1.0,
                        "query_used": query
                    })
                
                return structured_results
            except Exception as e:
                self.logger.error(f"Search failed: {str(e)}")
                return []

        self.tools = [web_search]
        
        # Configure agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional research assistant. 
             Perform thorough web research and return structured results with sources.
             Maintain original query intent while being flexible with spellings."""),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        self.agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

    async def run(self, query: str, user_id: str = "default") -> List[Dict[str, Any]]:
        """Execute research with spelling flexibility"""
        try:
            self.logger.info(f"Starting research for: {query}")
            research_results = []
            
            # First attempt - exact query
            result = await self.agent_executor.ainvoke({
                "input": query,
                "is_retry": False
            })
            
            # Extract results
            for step in result.get('intermediate_steps', []):
                if isinstance(step[1], list):
                    research_results.extend(step[1])
            
            # Second attempt - try corrected spelling if no results and contains "travily"
            if not research_results and "travily" in query.lower():
                corrected_query = query.lower().replace("travily", "tavily")
                self.logger.info(f"Trying corrected query: {corrected_query}")
                result = await self.agent_executor.ainvoke({
                    "input": corrected_query,
                    "is_retry": True
                })
                
                for step in result.get('intermediate_steps', []):
                    if isinstance(step[1], list):
                        research_results.extend(step[1])
                
                if research_results:
                    research_results.append({
                        "content": f"Note: Original query was '{query}'. Showing results for '{corrected_query}'",
                        "url": "",
                        "title": "Search Note",
                        "score": 0.5,
                        "query_used": corrected_query
                    })
            
            if not research_results:
                self.logger.warning("No research results found")
                return []
                
            self.logger.info(f"Research completed with {len(research_results)} sources")
            return research_results
            
        except Exception as e:
            self.logger.error(f"Research failed: {str(e)}", exc_info=True)
            return []
