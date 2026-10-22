# AWS Implementation Details for Submission

## AWS Services Used:
1. **Amazon Bedrock (Claude 3 Haiku)**: 
   - **Purpose**: Used to generate a "Smart Summary" for the family.
   - **Implementation**: The server takes a week's worth of medication adherence data and mood check-in notes, then prompts Bedrock to synthesize this into a warm, compassionate, and non-medical summary.
   - **Benefit**: Transforms raw percentages into human-centric insights.

2. **Amazon SNS (Simple Notification Service)**:
   - **Purpose**: Real-time urgent alerts for caregivers.
   - **Implementation**: Whenever the `report_missed_dose` tool is called, the server triggers an SNS publish event to a specific Topic ARN, which can be configured to send SMS or Emails to caregivers.
   - **Benefit**: Ensures that critical gaps in care are noticed immediately, not just when the caregiver checks the app.

## Deployment Strategy (Recommended for Beginner Budget):
- **Server**: AWS App Runner. 
  - Why: It handles the Docker container, scaling, and HTTPS certificates automatically. No need to manage EC2 instances.
- **Database**: Amazon RDS for PostgreSQL (Free Tier).
  - Why: Fully managed backups and high availability.
- **Cost**: Fits within the AWS Free Tier for the first 12 months for small-scale testing.
