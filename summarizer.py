import os 
from typing import List, Dict
# Used for extractive summarization in fallback mode
from sklearn.feature_extraction.text import TfidVectorizer
from sklearn.metrics.pairwise import linear_kernel

# APIs are unavailable / deterministic baseline
def _fallback_summary(chunks: List[str], max_sents: int = 6) -> str:
    docs = [c for c in chunks if c]

    if not docs:
        return "No content available."
    
    """ This converts text into numerical vectors using **️TF-IDF: 
    Words that appear often in one document but not everywhere get higher weight. 
    Common words like "the" get low weight. """
    vect = TfidVectorizer(stop_words="english")
    X = vect.fit_transform(docs)

    """ Measures how central each chunk is 
    Chunks similar to many others get higher scores
    Which sentences best represent the overall discussion """
    scores = linear_kernel(X, X).sum(axis=1).A1 # sentence centrality

    """ Picks the most important chunks
    Keeps original order (so the summary reads naturally) """
    idxs = scores.argsort()[::-1][:max_sents]
    selected = [docs[i] for i in sorted(idxs)]

    return " ".join(selected) # key sentences stitched together

def summarize_with_llm(company: str, chunks: List[str]) -> Dict[str, str]:
    """
    Returns dict with keys: 'executive' , 'competitors', 'swot'
    Uses OpenAI if OPENAI_API_KEY is set; else fallback
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        text = _fallback_summary(chunks)
        return {
            "executive": text,
            "competitors": "Meta; HTC; Samsung",
            "swot": (
                "Strengths: brand, build quality. "
                "Weaknesses: high price, limited enterprise tooling. "
                "Opportunities: AR productivity, partnerships. "
                "Threats: lower-cost competitors."
            )
        }
    
    # OpenAI path
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    joined = "\n\n".join(chunks[:12])
    system = (
        "You are a market analyst. Summarize concisely. "
        "Output three sections: Executive Summary (4-6 sentences), "
        "Competitors (semicolon-separated), and SWOT (one line per item)."
    )

    """ explicitly tell the LLM:
    What the context is 
    Exactly how to format the answer 
    This reduces hallucination and parsing errors."""
    user = f"Company: {company}\n\nContext:\n{joined}\n\nFormat:\nEXECUTIVE:\n...\nCOMPETITORS:\n...\nSWOT:\nS: ...\nW: ...\nO: ...\nT: ..."

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.3, # more factual, less creative
    )

    content = resp.choices[0].message.content.strip()

    # very light parsing 
    exec_txt = content
    comps = "Meta; HTC"
    swot = "S: ... W: ... O: ... T: ..."

    try:
        parts = content.split("COMPETITORS:")
        exec_txt = parts[0].replace("EXECUTIVE:", "").strip()
        rest = parts[1] if len(parts) > 1 else ""
        parts2 = rest.split("SWOT:")
        comps = parts2[0].strip().replace("\n", " ")
        swot = parts2[1].strip() if len(parts2) > 1 else ""

    except Exception:
        pass

    return {"executive": exec_txt, "competitors": comps, "swot": swot}
