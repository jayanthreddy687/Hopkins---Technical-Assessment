"""Application constants and enumerations."""

from enum import Enum
from typing import Dict, List


class DocumentCategory(str, Enum):
    """Document category enumeration."""
    
    FINANCIAL = "financial"
    LEGAL = "legal"
    COMMERCIAL = "commercial"
    OPERATIONS = "operations"
    OTHER = "other"


class AnalysisStatus(str, Enum):
    """Analysis status enumeration."""
    
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# Category keywords for document classification
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    DocumentCategory.FINANCIAL: [
        "revenue", "profit", "loss", "cash", "debt", "equity",
        "financial", "audit", "accounting", "budget", "forecast",
        "ebitda", "margins", "balance sheet", "income statement",
        "expenses", "assets", "liabilities", "capital"
    ],
    DocumentCategory.LEGAL: [
        "contract", "agreement", "terms", "conditions", "liability",
        "indemnity", "warranty", "compliance", "regulation", "legal",
        "law", "court", "litigation", "dispute", "clause", "covenant",
        "jurisdiction", "governing law", "arbitration"
    ],
    DocumentCategory.COMMERCIAL: [
        "customer", "client", "sales", "marketing", "pricing",
        "competition", "market", "brand", "product", "service",
        "revenue", "growth", "acquisition", "retention", "segment",
        "channel", "distribution", "partnership"
    ],
    DocumentCategory.OPERATIONS: [
        "process", "production", "manufacturing", "supply", "logistics",
        "quality", "safety", "environment", "facility", "equipment",
        "staff", "training", "procedure", "workflow", "inventory",
        "maintenance", "efficiency", "capacity"
    ]
}


# LLM Prompts
DOCUMENT_ANALYSIS_PROMPT_TEMPLATE = """You are a private-equity diligence analyst. Be concise, literal, and conservative. If unsure, say 'Unknown'. Output valid JSON only that matches the schema.

Return JSON for this document.

Document meta:
- filename: {filename}
- category: {category}

JSON schema:
{{
  "doc": "string",           // filename
  "category": "financial|legal|commercial|operations|other",
  "facts": ["string", ...],  // 1-5 bullets, short, objective
  "red_flags": ["string", ...] // 0-5 bullets, short, concrete risk statements
}}

Heuristics:
- Prefer explicit numbers, terms, durations, thresholds, parties, and dates.
- Red flags include: missing statements, exclusivity, unilateral termination, indemnities, breaches, going concern, overdue/arrears, covenants, related parties, churn, key-customer risk, safety/compliance issues, expired docs.

Document text (truncated):
{text}"""


SUMMARY_GENERATION_PROMPT_TEMPLATE = """You summarize for an Investment Committee. Group by category. Be concise and professional. 300–400 words.

Input is a JSON array of per-document results:
{analysis_json}

Write a single 300–400 word summary focusing on red flags first. Group by Financial, Legal, Operations, Commercial. Where helpful, reference counts (e.g., "3 red flags across two contracts")."""


RETRY_ANALYSIS_PROMPT_TEMPLATE = """Your last output was invalid JSON. Return only valid JSON matching the schema, no prose.

Document: {filename}
Category: {category}

Return JSON in this exact format:
{{
  "doc": "{filename}",
  "category": "{category}",
  "facts": ["fact1", "fact2"],
  "red_flags": ["flag1", "flag2"]
}}

Document text:
{text}"""

