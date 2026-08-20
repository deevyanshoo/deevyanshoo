from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Build:
    label: str
    detail: str


NAME = "DIVYANSHU GOYAL"
ROLE = "AI ARCHITECT // FOUNDER // BUILDER"
POSITIONING = "I build ambitious AI systems from first principles to production."
TAGLINE = "making large models fit small boxes"
LOCATION = "Gurugram ↔ wherever"
CURRENT_MISSION = "Nnomi — a financial friend for the full journey to wealth"
SECONDARY_MISSION = "Chauffit — an AI-powered, safety-first driver marketplace"

SELECTED_BUILDS = (
    Build("JARVIS", "hybrid + on-device inference on a phone"),
    Build("DAG LEDGER", "decentralized approvals without an ever-growing chain"),
    Build("AVIATION", "90%+ demand forecasting, 65 days ahead, ~800 TB/day"),
)
