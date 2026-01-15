from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
import re

app = FastAPI(
    title="Quantum-Ready Parsing Engine",
    description="Future-proof query parsing for AI and quantum search.",
    version="0.1.0"
)

# ---------- Data Models ----------

class RawQuery(BaseModel):
    query: str
    user_role: Optional[str] = "customer"   # e.g., "homeowner", "property_manager"
    location: Optional[str] = None          # e.g., "San Jose, CA"
    channel: Optional[str] = "web"          # e.g., "web", "phone", "sms"


class ParsedQuery(BaseModel):
    primary_intent: str                     # e.g., "plumbing_repair"
    service_type: Optional[str] = None      # e.g., "water_heater", "leak", "drain"
    urgency: Optional[str] = None           # e.g., "emergency", "same_day", "flexible"
    budget_sensitivity: Optional[str] = None# e.g., "low", "medium", "high"
    location: Optional[str] = None
    modifiers: Dict[str, str] = {}
    quantum_ready_vector: Optional[List[float]] = None  # placeholder for future quantum embedding


# ---------- Utility: Simple Rule-Based Parsing (MVP) ----------

SERVICE_KEYWORDS = {
    "plumber": "plumbing",
    "plumbing": "plumbing",
    "leak": "leak",
    "pipe": "leak",
    "drain": "drain",
    "toilet": "toilet",
    "roof": "roofing",
    "roofer": "roofing",
    "hvac": "hvac",
    "air conditioner": "hvac",
    "furnace": "hvac",
    "electrician": "electrical",
    "electrical": "electrical",
    "cement": "cement",
    "concrete": "cement",
}

URGENCY_KEYWORDS = {
    "now": "emergency",
    "asap": "emergency",
    "urgent": "emergency",
    "tonight": "emergency",
    "today": "same_day",
    "tomorrow": "soon",
    "whenever": "flexible",
}

BUDGET_KEYWORDS = {
    "cheap": "low",
    "affordable": "low",
    "budget": "low",
    "expensive": "high",
    "premium": "high",
    "fair price": "medium",
}

STOPWORDS = set([
    "i", "need", "a", "an", "the", "to", "for", "my", "in", "at", "on", "of",
    "please", "help", "with", "and", "is", "it", "that", "can", "you"
])


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_primary_intent(tokens: List[str]) -> str:
    # Very simple heuristic: map any service keyword to a normalized intent
    for t in tokens:
        if t in SERVICE_KEYWORDS:
            return SERVICE_KEYWORDS[t] + "_service"
    return "general_service"


def extract_service_type(tokens: List[str]) -> Optional[str]:
    # Could be more granular later
    for t in tokens:
        if t in ["leak", "drain", "toilet", "roof", "hvac", "cement", "concrete"]:
            return t
    return None


def extract_urgency(text: str) -> Optional[str]:
    for k, v in URGENCY_KEYWORDS.items():
        if k in text:
            return v
    return None


def extract_budget(text: str) -> Optional[str]:
    for k, v in BUDGET_KEYWORDS.items():
        if k in text:
            return v
    return None


def tokenize(text: str) -> List[str]:
    return [t for t in text.split() if t not in STOPWORDS]


def build_quantum_ready_vector(parsed: ParsedQuery) -> List[float]:
    """
    Placeholder for future quantum embedding / state prep.
    For now, we just encode a simple numeric representation.
    In the future, this could map to amplitudes or feature vectors
    used to initialize a quantum search or optimization routine.
    """
    # Simple categorical encoding as an example
    intent_map = {
        "plumbing_service": 0.1,
        "roofing_service": 0.2,
        "hvac_service": 0.3,
        "electrical_service": 0.4,
        "cement_service": 0.5,
        "general_service": 0.0,
    }
    urgency_map = {
        "emergency": 1.0,
        "same_day": 0.7,
        "soon": 0.5,
        "flexible": 0.2,
        None: 0.0,
    }
    budget_map = {
        "low": 0.2,
        "medium": 0.5,
        "high": 0.8,
        None: 0.0,
    }

    intent_val = intent_map.get(parsed.primary_intent, 0.0)
    urgency_val = urgency_map.get(parsed.urgency, 0.0)
    budget_val = budget_map.get(parsed.budget_sensitivity, 0.0)

    # Example vector: [intent, urgency, budget]
    return [intent_val, urgency_val, budget_val]


# ---------- API Endpoints ----------

@app.get("/")
def root():
    return {
        "message": "Quantum-Ready Parsing Engine is live.",
        "status": "ok",
        "version": "0.1.0"
    }


@app.post("/parse", response_model=ParsedQuery)
def parse_query(payload: RawQuery):
    """
    Core endpoint:
    - Takes a raw human query (e.g., 'I need a cheap plumber in San Jose ASAP')
    - Applies parsing rules
    - Returns a structured, quantum-ready representation
    """
    normalized = normalize(payload.query)
    tokens = tokenize(normalized)

    primary_intent = extract_primary_intent(tokens)
    service_type = extract_service_type(tokens)
    urgency = extract_urgency(normalized)
    budget = extract_budget(normalized)

    modifiers: Dict[str, str] = {}
    if payload.user_role:
        modifiers["user_role"] = payload.user_role
    if payload.channel:
        modifiers["channel"] = payload.channel

    parsed = ParsedQuery(
        primary_intent=primary_intent,
        service_type=service_type,
        urgency=urgency,
        budget_sensitivity=budget,
        location=payload.location,
        modifiers=modifiers,
    )

    # Attach quantum-ready vector (future: replace with real quantum prep)
    parsed.quantum_ready_vector = build_quantum_ready_vector(parsed)

    return parsed
