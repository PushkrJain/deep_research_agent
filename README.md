# Deep Research Agent

## Project Description
Deep Research Agent is an advanced AI-powered research system designed to perform comprehensive online information gathering and report generation. The system leverages a multi-agent architecture built with LangChain and LangGraph frameworks, integrating the Tavily API for web crawling and the Google Gemini API for natural language processing. The system consists of:

- **Research Agent**: Collects and structures data from web sources using Tavily's advanced search capabilities.
- **Draft Agent**: Generates detailed, well-structured research reports in markdown format.
- **Visualization Agent**: Creates visual representations of source reliability using Matplotlib and Seaborn.
- **Export Agent**: Saves reports in various formats, including Word documents with embedded visualizations.

The system is designed to handle complex research queries, and produce professional-grade reports with source citations and reliability visualizations.

## System Requirements
This project was developed and tested on Kali Linux. The following software is required:

- Python 3.10 or higher
- pip (Python package manager)
- A bash-compatible shell (e.g., Bash, Zsh)

## Directory Structure
```plain
deep_research_agent/
├── research/
│   ├── __init__.py
│   ├── research_agent.py        # Research agent for web crawling and data collection
│   ├── draft.py          # Draft agent for report generation
│   ├── visualize.py      # Visualization agent for reliability charts
│   └── export.py         # Export agent for saving reports
├── app.py                # Main application script
├── requirements.txt      # Project dependencies
├── LICENSE               # License file
└── README.md             # Project documentation
```

## Setup Instructions
Follow these steps to set up and run the Deep Research Agent on your Kali Linux system.

### 1. Clone the Repository
```bash
git clone https://github.com/PushkrJain/deep_research_agent.git
cd deep-research-agent
```

### 2. Install Dependencies
Ensure Python 3.10+ and pip are installed. Then, install the required Python packages listed in requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. Obtain API Keys
The project requires two API keys:
- Tavily API Key:
    - Sign up at [Tavily](https://app.tavily.com/home) to obtain an API key.
    - The key is used for web search and data collection.
- Google Gemini API Key:
    - Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).
    - The key is used for the Gemini model in LangChain for report generation.

### 4. Set Environment Variables
Set the API keys as environment variables in your bash shell. Add the following lines to your `~/.bashrc` or `~/.zshrc`:
```bash
export TAVILY_API_KEY="your-tavily-api-key"
export GOOGLE_API_KEY="your-google-api-key"
```

Apply the changes:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Alternatively, set the variables for the current session only:
```bash
export TAVILY_API_KEY="your-tavily-api-key"
export GOOGLE_API_KEY="your-google-api-key"
```

### 5. Run the Application
Start the interactive research interface:
```bash
python app.py
```

The system will prompt you to enter a research question. Type your query, and the system will:
- Perform web research using the Research Agent.
- Generate a reliability visualization using the Visualization Agent.
- Draft a comprehensive report using the Draft Agent.
- Save the report as a Word document with embedded visualizations using the Export Agent.

Type `exit` to quit.

### 6. Output
Reports and visualizations are saved in the `./research_outputs` directory, with filenames including timestamps (e.g., `report_20250425_123456.docx`, `reliability_20250425_123456.png`). Error logs are saved to `research.log`.

**Usage Example**

![Image](https://github.com/user-attachments/assets/24dae013-5cfd-4682-8038-d40741381e37)

![Image](https://github.com/user-attachments/assets/62ed144e-510d-420f-acb2-ec509e26c2ef)

**Generated Report Preview**

![Screenshot From 2025-04-25 19-35-59](https://github.com/user-attachments/assets/2aa6a6cd-d4a0-4b7b-85a4-2957cc62fbeb)

![Screenshot From 2025-04-25 19-36-33](https://github.com/user-attachments/assets/6a565102-aa17-4932-a94e-c83be4ae31e6)

### Troubleshooting
- **API Key Errors:**
  Ensure `TAVILY_API_KEY` and `GOOGLE_API_KEY` are set correctly. Check with
  
  ```bash
  echo $TAVILY_API_KEY
  echo $GOOGLE_API_KEY
  ```
- **Dependency Issues:**
  Verify all packages are installed
  ```bash
  pip list
  ```
  update pip if needed 
  ```bash
  pip install --upgrade pip
  ```
- **No Results:**
  Check your internet connection and ensure the query is specific enough. The system logs errors to `research.log` for debugging.

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgments
- Built with LangChain and LangScale for agent orchestration.
- Powered by Tavily for web search and Google Gemini for language modeling.
- Visualizations created using Matplotlib and Seaborn.
