
import os

import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

from src.database.connection import SessionLocal, init_db
from src.database.queries import (
    get_todays_medications,
    log_dose,
    create_missed_dose_alert,
    add_checkin,
    get_weekly_summary,
    get_emotional_trend,
)

load_dotenv()

mcp = FastMCP(
    "Caregiver Companion",
    host="0.0.0.0",
    port=8000,
)

API_TOKEN = os.getenv("MCP_SERVER_TOKEN", "default-secret-token")


def verify_token(token: str) -> None:
    """Reject requests with an invalid or missing authentication token."""
    if not token or token != API_TOKEN:
        raise PermissionError("Invalid or missing authentication token.")


@mcp.tool()
def get_todays_meds(
    patient_id: str,
    token: str = "default-secret-token",
) -> str:
    """Fetch today's scheduled medications, including dosage and time."""
    verify_token(token)

    with SessionLocal() as db:
        meds = get_todays_medications(db, patient_id)

        if not meds:
            return "No medications scheduled for today."

        response = "Here are today's medications:\n"

        for med in meds:
            response += (
                f"- {med['medication']} ({med['dosage']}) "
                f"at {med['time']}\n"
            )

        return response


@mcp.tool()
def log_dose_taken(
    schedule_id: str,
    token: str = "default-secret-token",
) -> str:
    """Record a medication dose reported as taken."""
    verify_token(token)

    with SessionLocal() as db:
        try:
            log_dose(db, schedule_id)
            return "Dose recorded! Great job staying on track."
        except ValueError as exc:
            return str(exc)


@mcp.tool()
def report_missed_dose(
    schedule_id: str,
    reason: str = "Unknown",
    token: str = "default-secret-token",
) -> str:
    """Report a missed dose and trigger the caregiver alert workflow."""
    verify_token(token)

    with SessionLocal() as db:
        return create_missed_dose_alert(db, schedule_id, reason)


@mcp.tool()
def daily_health_checkin(
    patient_id: str,
    mood: int,
    notes: str,
    token: str = "default-secret-token",
) -> str:
    """Record the patient's daily mood score from 1 to 5."""
    verify_token(token)

    if not 1 <= mood <= 5:
        return "Mood must be an integer between 1 and 5."

    with SessionLocal() as db:
        return add_checkin(db, patient_id, mood, notes)


@mcp.tool()
def get_family_summary(
    patient_id: str,
    token: str = "default-secret-token",
) -> str:
    """Return adherence statistics and a seven-day summary."""
    verify_token(token)

    with SessionLocal() as db:
        summary = get_weekly_summary(db, patient_id)

        return (
            f"Weekly Adherence: {summary['adherence_rate']}\n"
            f"Doses: {summary['taken_doses']} taken, "
            f"{summary['missed_doses']} missed.\n"
            f"Note: {summary['summary']}"
        )


@mcp.tool()
def get_emotional_health_trend(
    patient_id: str,
    token: str = "default-secret-token",
) -> str:
    """Summarize emotional trends from daily check-in notes."""
    verify_token(token)

    with SessionLocal() as db:
        return get_emotional_trend(db, patient_id)


if __name__ == "__main__":
    init_db()

    app = mcp.streamable_http_app()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5500",
            "http://127.0.0.1:5500",
        ],
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "Content-Type",
            "Accept",
            "MCP-Protocol-Version",
            "MCP-Session-Id",
            "Last-Event-ID",
        ],
        expose_headers=[
            "MCP-Session-Id",
            "MCP-Protocol-Version",
        ],
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
    )
