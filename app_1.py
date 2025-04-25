#!/usr/bin/env python3
import os
import sys
import asyncio
import datetime
import logging
from typing import TypedDict, List, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from research_agent_1 import ResearchAgent
from draft_agent_1 import DraftAgent
from visualize_1 import VisualizationAgent
from export_1 import Exporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('research.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
DEFAULT_OUTPUT_DIR = "./research_outputs"
os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)

# Disable verbose outputs
os.environ["LANGCHAIN_VERBOSE"] = "false"
os.environ["TAVILY_VERBOSE"] = "false"

class ResearchState(TypedDict):
    query: str
    research_results: List[Dict[str, Any]]
    visualization_path: Optional[str]
    report: Dict[str, Any]
    error: Optional[str]

async def research_node(state: ResearchState) -> Dict[str, Any]:
    """Execute research and collect data"""
    try:
        logger.info(f"Starting research for: {state['query']}")
        agent = ResearchAgent(model="gemini-1.5-pro-latest")
        results = await agent.run(state["query"])
        
        if not results:
            logger.warning("No research results returned")
            return {"research_results": [], "error": "No research data found"}
            
        logger.info(f"Research completed with {len(results)} sources")
        return {"research_results": results, "error": None}
    except Exception as e:
        logger.error(f"Research failed: {str(e)}", exc_info=True)
        return {"research_results": [], "error": f"Research failed: {str(e)}"}

async def visualize_node(state: ResearchState) -> Dict[str, Any]:
    """Generate visualizations from research data"""
    try:
        if not state.get("research_results"):
            raise ValueError("No research data for visualization")
        
        logger.info("Generating reliability visualization")
        viz_agent = VisualizationAgent()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(DEFAULT_OUTPUT_DIR, f"reliability_{timestamp}.png")
        
        viz_agent.plot_reliability(
            state["research_results"],
            filename=image_path
        )
        
        logger.info(f"Visualization saved to {image_path}")
        return {"visualization_path": image_path, "error": None}
    except Exception as e:
        logger.error(f"Visualization failed: {str(e)}", exc_info=True)
        return {"visualization_path": None, "error": f"Visualization failed: {str(e)}"}

async def draft_node(state: ResearchState) -> Dict[str, Any]:
    """Generate report from research data"""
    try:
        if not state.get("research_results"):
            raise ValueError("No research data")

        logger.info("Generating research report")
        agent = DraftAgent(model="gemini-1.5-pro-latest")
        report = await agent.generate_report(
            state["query"],
            state["research_results"]
        )
        return {"report": report, "error": None}
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}", exc_info=True)
        return {
            "report": {
                "question": state["query"],
                "answer": f"Could not generate answer: {str(e)}",
                "sources": [],
                "query_variations": []
            },
            "error": f"Drafting failed: {str(e)}"
        }

def create_workflow() -> Any:
    """Create research workflow with visualization"""
    workflow = StateGraph(ResearchState)
    workflow.add_node("research", research_node)
    workflow.add_node("visualize", visualize_node)
    workflow.add_node("draft", draft_node)
    
    workflow.set_entry_point("research")
    workflow.add_edge("research", "visualize")
    workflow.add_edge("visualize", "draft")
    workflow.add_edge("draft", END)
    
    return workflow.compile()

async def run_pipeline(query: str) -> Dict[str, Any]:
    """Execute complete research pipeline"""
    logger.info(f"Starting pipeline for query: {query}")
    app = create_workflow()
    try:
        results = await app.ainvoke({
            "query": query,
            "research_results": [],
            "visualization_path": None,
            "report": {},
            "error": None
        })

        if not results.get("report"):
            raise ValueError("No report generated")

        # Save report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, f"report_{timestamp}.docx")

        Exporter.to_word(
            content_text=results["report"]["answer"],
            image_path=results.get("visualization_path"),
            sources=results["report"].get("sources", []),
            filename=output_path
        )

        return {
            "success": True,
            "answer": results["report"]["answer"],
            "path": output_path,
            "sources": len(results["report"].get("sources", [])),
            "visualization": results.get("visualization_path") is not None,
            "query_variations": results["report"].get("query_variations", [])
        }
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        
        # Generate error report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        error_path = os.path.join(DEFAULT_OUTPUT_DIR, f"error_report_{timestamp}.txt")
        
        with open(error_path, 'w') as f:
            f.write(f"Research failed for query: {query}\n")
            f.write(f"Error: {str(e)}\n")
            f.write("\nSuggestions:\n")
            f.write("- Check your query spelling\n")
            f.write("- Verify your API keys are valid\n")
            f.write("- Check your internet connection\n")
        
        return {
            "success": False,
            "answer": f"Research failed. Error report saved to {error_path}",
            "path": error_path,
            "sources": 0,
            "visualization": False,
            "query_variations": []
        }

async def interactive_session():
    """Interactive research interface"""
    print("\n🔍 Research Assistant (type 'exit' to quit)")
    print("-----------------------------------------")
    print("Note: Both exact queries and common variations will be searched")
    print("-----------------------------------------")
    logger.info("Starting interactive session")

    while True:
        try:
            query = input("\nEnter your research question: ").strip()
            if query.lower() in ("exit", "quit"):
                logger.info("Session ended by user")
                break

            if not query:
                continue

            print("\n🔄 Processing your request...")
            result = await run_pipeline(query)

            print("\n" + "="*60)
            if result["success"]:
                print(f"📝 Research Question: {query}")
                print("\n🔎 Findings:")
                print(result["answer"])
                print(f"\n📄 Report saved to: {result['path']}")
                print(f"🔗 Sources used: {result['sources']}")
                if result["visualization"]:
                    print("📊 Reliability visualization included")
                if len(result["query_variations"]) > 1:
                    print(f"\nℹ️ Note: Searched variations: {', '.join(result['query_variations'])}")
            else:
                print("❌ Research failed")
                print(f"Details: {result['answer']}")
            print("="*60)

        except KeyboardInterrupt:
            logger.info("Session ended by keyboard interrupt")
            print("\nSession ended")
            break

if __name__ == "__main__":
    try:
        # Check required environment variables
        if not os.getenv("TAVILY_API_KEY"):
            logger.error("TAVILY_API_KEY environment variable is required")
            print("Error: TAVILY_API_KEY environment variable is required")
            sys.exit(1)
        if not os.getenv("GOOGLE_API_KEY"):
            logger.error("GOOGLE_API_KEY environment variable is required")
            print("Error: GOOGLE_API_KEY environment variable is required")
            sys.exit(1)
            
        asyncio.run(interactive_session())
    except Exception as e:
        logger.error(f"System error occurred: {str(e)}", exc_info=True)
        print(f"System error occurred: {str(e)}")
        sys.exit(1)
