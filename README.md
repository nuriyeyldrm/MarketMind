# MarketMind: AI-Powered Market Intelligence Assistant  

MarketMind is an LLM-powered system that automates market research and competitive analysis.  
Given a company or product name, it gathers live public data, analyzes sentiment and trends, and generates an executive-style insight report — in minutes.  

---

## Overview
**Problem:** Manual market research is slow, inconsistent, and often limited by human bias.  
**Solution:** MarketMind automates this process with Retrieval-Augmented Generation (RAG), combining real-time data collection and large language model reasoning to deliver structured, explainable business insights.  

**Key Features**
- **Live Data Retrieval:** Integrates with NewsAPI and Reddit API to collect relevant articles and discussions.  
- **LLM Summarization:** Uses GPT-4 (or open models like Mistral) to summarize and extract key business signals.  
- **Visualization Dashboard:** Interactive Streamlit dashboard with sentiment charts and keyword trends.  
- **SWOT Analysis:** Automatically identifies Strengths, Weaknesses, Opportunities, and Threats from the data.  
- **Report Generation:** One-click export of an executive summary in PDF format.  
- **Extensible Design:** Modular code structure for adding new data sources or visualizations.  

---

## System Architecture
```mermaid
flowchart TD
  A[User Input: Company or Product] --> B[Data Fetcher: NewsAPI, Reddit]
  B --> C[Preprocessor: Clean and Chunk Text]
  C --> D[Vector Store: Chroma or FAISS]
  D --> E[LLM Summarizer: GPT-4 or Mistral]
  E --> F[Insight Generator: SWOT and Sentiment]
  F --> G[Dashboard and PDF Report]
