import os
import io 
import plotly.express as px # makes the keyword bar chart
import streamlit as st # Streamlit UI components
from dotenv import load_dotenv

from data_fetcher import fetch_newsapi, fetch_reddit
from utils import clean_text, chunk_text, keyword_frequency
from summarizer import summarize_with_llm
from report_generator import build_markdown_report

load_dotenv() # loads .env file variables locally

# Streamlit page settings and title
st.set_page_config(page_title="MarketMind", page_icon="🧠", layout="wide")
st.title("🧠 MarketMind — AI-Powered Market Intelligence Assistant")

""" Adds a sidebar switch: "Demo mode"
Default value depends on whether you have a NewsAPI key"""
with st.sidebar:
    st.markdown("**Mode**")
    demo_mode = st.toggle("Demo mode (no APIs)", value=not bool(os.getenv("NEWS_API_KEY")))
    st.markdown("---")
    st.caption("Tip: add API keys in a '.env' file to fetch live data.")

company = st.text_input("Company or product name", value="Apple Vision Pro") # Collects the company name
run = st.button("Generate Insight Report") # Button triggers the pipeline

# Only runs when the user clicks button and company is not empty
if run and company.strip():
    with st.spinner("Collecting and analyzing data..."):
        # 1) Fetch data
        news = fetch_newsapi(company) if not demo_mode else fetch_newsapi("") # demo returns static
        reddit = fetch_reddit(company)

        # Normalize text documents into list of strings
        docs = []

        for a in news + reddit:
            text = clean_text(f"{a.get('title','')}.{a.get('content','')}")

            if text:
                docs.append(text)

        # 2) Chunk & summarize (LLMs work better with chunks than extremely long text)
        chunks = []

        for d in docs: 
            chunks.extend(chunk_text(d, max_chars=900)) # Each document produces multiple chunks

        summary = summarize_with_llm(company, chunks) # Summarize using LLM or fallback

        # 3) Keyword frequency + chart
        """ Finds top words that appear frequently across the documents
        Creates a bar chart"""
        kw = keyword_frequency(docs, top_k=15)

        if kw:
            words, counts = zip(*kw)
            fig = px.bar(x=list(words), y=list(counts), labels={"x": "Keyword", "y": "Count"}, title="Keyword Frequency")
        
        else: 
            fig = px.bar(x=[], y=[], title="No keywords")

        # 4) Layout
        col1, col2 = st.columns([2,1]) # two-column dashboard

        with col1: # Left side (bigger): summary + SWOT
            st.subheader("Executive Summary")
            st.write(summary["executive"])
            st.subheader("SWOT")
            st.write(summary["swot"])
        
        with col2: # Right side: competitors + chart
            st.subheader("Competitors")
            st.write(summary["competitors"])
            st.plotly_chart(fig, use_container_width=True)

        # 5) Download report (Markdown for now)
        md = build_markdown_report(company, summary["executive"], summary["competitors"], summary["swot"], kw)
        st.download_button(
            "⬇️ Download Markdown Report",
            data=md.encode("utf-8"),
            file_name=f"marketmind_{company.replace(' ','_').lower()}.md",
            mime="text/markdown"
        )

        st.success("Done!")
