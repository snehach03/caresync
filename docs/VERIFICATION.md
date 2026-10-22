# MCP Verification Guide

This document explains how to verify the Caregiver Companion MCP server is working correctly using the MCP Inspector.

## 1. Start the Server
The easiest way to run the server is via Docker Compose:
\`\`\`bash
docker-compose up --build
\`\`\`

The server will be running at: `http://localhost:8000`

## 2. Run MCP Inspector
The MCP Inspector is the official tool for testing MCP servers. You can run it using npx:

\`\`\`bash
npx @modelcontextprotocol/inspector http://localhost:8000/sse
\`\`\`

## 3. Test Scenarios to Verify
Once the Inspector is open in your browser, try these steps:

### Scenario A: Patient Log a Dose
1. Use `get_todays_meds` with a test `patient_id`.
2. Copy a `schedule_id` from the result.
3. Call `log_dose_taken` using that `schedule_id`.
4. **Verify**: Call `log_dose_taken` again immediately. It should return the "15 minute" guardrail error.

### Scenario B: Missed Dose Alert
1. Call `report_missed_dose` with a `schedule_id` and a reason (e.g., "Patient forgot").
2. **Verify**: In the database (or via a future tool), check that an `Alert` was created for the caregiver.

### Scenario C: Weekly Summary
1. Call `get_family_summary` with the `patient_id`.
2. **Verify**: The adherence percentage is calculated correctly based on the logs you just created.

## 4. Authentication
All tools now require a `token` argument. 
- Use the token found in your `.env` file (default: `default-secret-token`).
- Try calling a tool with a wrong token to verify it returns a `PermissionError`.
