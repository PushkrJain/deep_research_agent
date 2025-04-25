# Deep Research Agent  

## Project Description  
Deep Research Agent is an advanced AI-powered research system designed to perform comprehensive online information gathering and report generation. The system leverages a multi-agent architecture built with LangChain and LangGraph frameworks, integrating the Tavily API for web crawling and the Google Gemini API for natural language processing. The system consists of:  

- **Research Agent**: Collects and structures data from web sources using Tavily's advanced search capabilities.  
- **Draft Agent**: Generates detailed, well-structured research reports in markdown format.  
- **Visualization Agent**: Creates visual representations of source reliability using Matplotlib and Seaborn.  
- **Export Agent**: Saves reports in various formats, including Word documents with embedded visualizations.  

The system is designed to handle complex research queries, correct spelling errors (e.g., "travily" to "tavily"), and produce professional-grade reports with source citations and reliability visualizations.  

## System Requirements  
This project was developed and tested on Kali Linux. The following software is required:  

- Python 3.10 or higher  
- pip (Python package manager)  
- A bash-compatible shell (e.g., Bash (recommended), Zsh)  

## Directory Structure  
deep-research-agent/
├── research_agent/
│ ├── init.py
│ ├── research.py # Research agent for web crawling and data collection
│ ├── draft.py # Draft agent for report generation
│ ├── visualize.py # Visualization agent for reliability charts
│ └── export.py # Export agent for saving reports
├── app.py # Main application script
├── requirements.txt # Project dependencies
├── LICENSE # License file
└── README.md # Project documentation

## Setup Instructions  
Follow these steps to set up and run the Deep Research Agent on your Kali Linux system.  

### 1. Clone the Repository  
```bash
git clone https://github.com/your-username/deep-research-agent.git
cd deep-research-agent

    Built with LangChain and LangScale for agent orchestration.

    Powered by Tavily for web search and Google Gemini for language modeling.

    Visualizations created using Matplotlib and Seaborn.
