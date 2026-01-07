from typing import List, Dict

# Markdown now; PDF in M6
def build_markdown_report(company: str, executive: str, competitors: str, swot: str, top_keywords):
    md = [f"# MarketMind Report — {company}\n"]
    md.append("## Executive Summary\n")
    md.append(executive + "\n")
    md.append("## Competitors\n")
    md.append(competitors + "\n")
    md.append("## SWOT\n")
    md.append(swot + "\n")
    md.append("## Top Keywords\n")
    for w,c in top_keywords:
        md.append(f"- {w}")
    
    return "\n".join(md)
