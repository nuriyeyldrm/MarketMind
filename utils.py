import re
from typing import List, Tuple, Dict
from collections import Counter

# Normalize messy text
def clean_texxt(text: str) -> str:
    if not text: # Handles empty text
        return ""
    
    text = re.sub(r"\s+", " ", text) # Replaces multiple spaces or line breaks with one space
    text = re.sub(r"[^\x00-\x7F]+", " ", text) # Removes non-ASCII characters (like emojis or special symbols)
    
    return text.strip() # Removes spaces at the beginning and end

""" Split text for LLM processing - LLMs (like GPT-4) can only process limited-length text at a time.
This function splits long text into smaller chunks, ideally by sentence, so the LLM can handle them efficiently."""
def chunk_text(text: str, max_chars: int = 1200) -> List[str]:
    text = clean_text(text)
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + max_chars, len(text))
        # Finds the last period before the chunk limit, so it doesn’t cut sentences in the middle
        period = text.rfind(".", start, end)
        
        if period == -1 or period < start + int(max_chars * 0.6): # If no period is found, it just slices at the limit
            period = end
        
        chunks.append(text[start:period].strip())
        start = period + 1
    
    return [c for c in chunks if c]

# Extract top keywords - This function finds the most frequent keywords in all documents (news, Reddit posts, etc.).    
def keyword_frequency(docs: List[str], top_k: int = 15) -> List[Tuple[str, int]]:
    words = []
    
    for d in docs: 
        tokens = re.findall(r"[A-Za-z]{3,}", d.lower()) # Finds all alphabetic words with >= 3 letters
        words.extend(tokens)
    
    stop = set("""
        the a an and or for with from into of in on to this that these those
        is are was were be been being as by at it its their his her they you we our your
        about over under within without not will would can could should may might
        product company market price sales customers growth new
    """.split()) # Common useless words to ignore
    
    words = [w for w in words if w not in stop]
    
    return Counter(words).most_common(top_k) # Counts occurrences and returns top k keywords