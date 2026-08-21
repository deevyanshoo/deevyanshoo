from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JourneyStep:
    label: str
    emphasis: str


NAME = "DIVYANSHU GOYAL"
ROLE = "AI ARCHITECT \u00b7 FOUNDER \u00b7 BUILDER"
TAGLINE = "making large models fit small boxes"
LOCATION = "Gurugram \u2194 wherever"
EDUCATION = (
    "MASTER OF SCIENCE IN ENGINEERING \u00b7 DATA SCIENCE "
    "\u00b7 UNIVERSITY OF PENNSYLVANIA"
)
WORK = "AI ARCHITECT @ ZS"

MISSION_NAME = "NNOMI"
MISSION_URL = "NNOMI.COM"
MISSION_LINE = "India-first financial coach for earning money \u2192 building wealth."
MISSION_JOURNEY = (
    JourneyStep("EARN", "income"),
    JourneyStep("SEE CLEARLY", "decisions"),
    JourneyStep("PROTECT", "safety net"),
    JourneyStep("INVEST", "growth"),
    JourneyStep("BUILD WEALTH", "long game"),
)

EASTER_EGGS = (
    "coffee ........ required",
    "runtime ........ v26",
    "inference ..... local > cloud",
    "garage_target .. 911",
)
