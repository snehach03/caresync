# 📝 Submission Templates

## DESCRIPTION.md (Draft)
**Project Name**: Caregiver Companion
**Track**: Alexa+ (Self-hosted MCP)

**What it does**: 
Caregiver Companion is a voice-first health assistant that helps elderly patients manage medications and enables family caregivers to monitor adherence in real-time.

**How it works**: 
Built on the Model Context Protocol (MCP), the system uses a Python-based server that exposes tools for medication logging and health check-ins. It integrates Amazon SNS for immediate missed-dose alerts and Amazon Bedrock (Claude 3 Haiku) to synthesize raw health data into empathetic weekly summaries.

**Key Technical Achievements**:
- Streamable HTTP transport for remote AI access.
- Timezone-aware PostgreSQL schema for global accessibility.
- Safety guardrails to prevent double-dosing.

---

## DEMO_SCRIPT.md (Video Guide)
**Total Duration**: < 3 minutes.

1. **The Hook (0:00-0:30)**: 
   - Show the `demo.html` interface. 
   - Voice Command: "Alexa, what do I take today?"
   - Result: Server returns the meds; AI speaks them warmly.
2. **The Crisis (0:30-1:30)**:
   - Voice Command: "I missed my morning pill."
   - Show the MCP Inspector logging the `report_missed_dose` call.
   - Show a simulated SNS notification appearing on a phone.
3. **The Insight (1:30-2:30)**:
   - Voice Command: "Give my daughter the weekly summary."
   - Result: Show the Bedrock-generated empathetic summary.
4. **The Tech (2:30-3:00)**:
   - Quick flash of the `docker-compose.yml` and `server.py`.
   - Closing statement on impact.

---

## SUBMISSION_CHECKLIST.md
- [x] Self-hosted MCP Server (Spec 2025-11-25)
- [x] Streamable HTTP Transport
- [x] Official Python MCP SDK
- [x] PostgreSQL Database with TIMESTAMPTZ
- [x] Voice-First Demo Page (STT/TTS)
- [x] MCP Inspector Verification
- [x] MIT License
- [x] AWS Integration 1: Amazon SNS (Alerts)
- [x] AWS Integration 2: Amazon Bedrock (Summaries)
- [x] Safety Note in README & UI
- [x] No third-party trademarks/copyrighted assets
