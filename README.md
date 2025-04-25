# 🤖 Deep Research Agent

**Deep Research Agent** is an advanced AI-powered research system designed to perform comprehensive online information gathering and professional-grade report generation. It uses a multi-agent architecture built with **LangChain** and **LangGraph**, integrating:

- 🌐 **Tavily API** – for powerful web crawling and data extraction  
- ✨ **Google Gemini API** – for natural language processing and response generation

---

## 🧠 System Overview

The system is structured into modular agents:

- **🔍 Research Agent:** Collects and structures data using Tavily’s advanced search.
- **📝 Draft Agent:** Generates detailed, markdown-formatted research reports.
- **📊 Visualization Agent:** Creates charts visualizing source reliability using Matplotlib and Seaborn.
- **📁 Export Agent:** Converts reports to Word documents with embedded visualizations.

It handles spelling corrections (e.g., “travily” → “tavily”), citation generation, and reliable source tagging.

---

## 🖥️ System Requirements

- **Operating System:** Tested on Kali Linux
- **Python:** 3.8 or higher
- **Shell:** Bash-compatible (e.g., Bash, Zsh)
- **Package Manager:** pip

---

## 📁 Directory Structure

deep-research-agent/ ├── research_agent/ │ ├── init.py │ ├── research.py # Research Agent │ ├── draft.py # Draft Agent │ ├── visualize.py # Visualization Agent │ └── export.py # Export Agent ├── app.py # Main interface script ├── requirements.txt # Dependencies ├── LICENSE └── README.md


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/deep-research-agent.git
cd deep-research-agent

2. Install Dependencies

Ensure Python 3.8+ and pip are installed, then run:

pip install -r requirements.txt

requirements.txt includes:

    langchain

    langgraph

    openai

    matplotlib

    python-docx

    markdown2

    google-generativeai

    langchain-google-genai

    seaborn

3. Obtain API Keys
Tavily API Key

    Sign up at Tavily and obtain your API key.

    Used for web search and data collection.

Google Gemini API Key

    Get your API key from Google AI Studio.

    Used for generating responses using the Gemini model.

4. Set Environment Variables

Add the following to your ~/.bashrc or ~/.zshrc:

export TAVILY_API_KEY="your-tavily-api-key"
export GOOGLE_API_KEY="your-google-api-key"

Apply changes:

source ~/.bashrc   # or source ~/.zshrc

Or for current session only:

export TAVILY_API_KEY="your-tavily-api-key"
export GOOGLE_API_KEY="your-google-api-key"

5. Run the Application

python app.py

The system will:

    Collect data via Tavily

    Generate a reliability chart

    Draft a report in Markdown

    Export it as a Word document with visuals

To exit: type exit or quit
📂 Output

    Saved to: ./research_outputs/

    Formats: .docx with timestamped filenames (e.g., report_20250425_123456.docx)

    Visual charts: reliability_20250425_123456.png

    Logs: research.log for errors/debugging

🚀 Usage Example

$ python app.py

🔍 Research Assistant (type 'exit' to quit)
-----------------------------------------
Note: Both exact queries and common variations will be searched
-----------------------------------------

Enter your research question: What is the impact of AI on healthcare?
🔄 Processing your request...

============================================================
📝 Research Question: What is the impact of AI on healthcare?
🔎 Findings:
[Generated report content...]
📄 Report saved to: ./research_outputs/report_20250425_123456.docx
🔗 Sources used: 5
📊 Reliability visualization included
============================================================

🛠️ Troubleshooting

    API Key Errors:
    Check with echo $TAVILY_API_KEY and echo $GOOGLE_API_KEY

    Dependencies Missing:
    Ensure packages are installed: pip list
    Update pip: pip install --upgrade pip

    No Results Found:

        Check your internet connection

        Try making your query more specific

        Check research.log for debugging details

🤝 Contributing

Contributions are welcome!

    Fork the repo

    Create a feature branch:

git checkout -b feature/your-feature

Commit your changes:

git commit -m "Add your feature"

Push the branch:

    git push origin feature/your-feature

    Open a Pull Request

📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
🙏 Acknowledgments

    Built with LangChain and LangGraph for agent orchestration

    Powered by Tavily for intelligent search

    Enhanced by Google Gemini for natural language generation

    Visualized using Matplotlib and Seaborn
