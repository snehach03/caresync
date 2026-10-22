# 💊 Caregiver Companion

**A Voice-First MCP Server for Elderly Care & Medication Management**

> **⚠️ SAFETY NOTE:** This is a reminder and tracking tool, NOT a medical device. It does not provide medical advice, diagnosis, or dose changes. Always consult a licensed healthcare professional for medical decisions.

Caregiver Companion is an AI-powered system designed to bridge the gap between older adults and their caregivers. By utilizing the **Model Context Protocol (MCP)**, it allows a voice-first interface (like Alexa+) to manage medications, track daily health check-ins, and alert family members in real-time.

## ✨ Key Features

- **Voice-First Interaction**: Designed for accessibility, allowing patients to log doses and report mood via simple voice commands.
- **Real-time Alerts**: Integrated with **Amazon SNS** to notify caregivers immediately when a dose is missed.
- **AI Smart Summaries**: Uses **Amazon Bedrock (Claude 3 Haiku)** to transform raw adherence data into warm, empathetic weekly summaries for the family.
- **Secure Architecture**: Implements bearer-token authentication and a robust PostgreSQL backend with timezone-aware timestamps.

## 🚀 Quick Start (One-Command Run)

### Prerequisites
- Docker and Docker Compose installed.

### Execution
1. Clone the repository.
2. Copy the environment template:
   \`\`\`bash
   cp .env.example .env
   \`\`\`
3. Start the entire stack:
   \`\`\`bash
   docker-compose up --build
   \`\`\`

The server will be available at `http://localhost:8000`.

## 🛠️ Technical Architecture

- **Transport**: Streamable HTTP (MCP Spec 2025-11-25).
- **Backend**: Python 3.11 / FastMCP SDK.
- **Database**: PostgreSQL 16 (via SQLAlchemy 2.0).
- **Cloud**: AWS SNS (Alerts), AWS Bedrock (Summaries).
- **Demo**: HTML5/JS with Web Speech API (STT/TTS).

## 🧪 Testing & Verification

1. **MCP Inspector**: Run \`npx @modelcontextprotocol/inspector http://localhost:8000/sse\` to verify tool calls.
2. **Web Demo**: Open `demo.html` in a modern browser to experience the voice-first flow.
3. **API Tests**: Run \`pytest\` to execute the backend test suite.
