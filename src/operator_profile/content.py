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
LOCATION = "Gurugram <-> wherever"

CURRENT_MISSION = "NNOMI"
CURRENT_MISSION_URL = "nnomi.com"
CURRENT_MISSION_LINE_1 = "A financial coach for the entire journey"
CURRENT_MISSION_LINE_2 = "from earning money to building wealth."
SECONDARY_MISSION = "CHAUFFIT // safety-first on-demand driver marketplace"

SELECTED_BUILDS = (
    Build("JARVIS", "hybrid inference: local SLM + cloud LLM"),
    Build("DAG LEDGER", "peer-approved blocks + custom consensus"),
    Build("AVIATION", ">90% forecast accuracy // D+65 // ~800 TB/day"),
)
