# deep-research-agent
Automated web research &amp; report generation using LangGraph. Crawls data (Tavily), scores reliability (0-1), and drafts structured reports (Word/CSV/JSON) with Gemini. Features dual-agent workflow, interactive CLI, and source visualization. Perfect for academics/analysts needing auditable research.  Stack: Python, LangChain, Gemini, Matplotlib

**Project Structure**
deep-research-agent/  
├── .github/  
│   └── workflows/  
│       └── tests.yml          # CI/CD (optional)  
├── research_agent/  
│   ├── __init__.py  
│   ├── research_agent.py     # ResearchAgent  
│   ├── draft_agent.py        # DraftAgent  
│   ├── visualize.py          # VisualizationAgent  
│   ├── export.py             # Exporter  
│   └── utils.py              # Helper functions  
├── tests/  
│   ├── test_research.py      # Pytest cases  
│   └── test_draft.py  
├── outputs/                  # Auto-generated reports  
├── docs/  
│   ├── ARCHITECTURE.md       # System design  
│   └── WORKFLOW.md           # Graph flow  
├── requirements.txt  
├── app.py                    # CLI entry point  
└── README.md                 # Project showcase  
