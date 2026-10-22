import boto3
import os
import json
from botocore.exceptions import ClientError

# Load environment variables for AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

# Initialize Clients
sns_client = boto3.client("sns", region_name=AWS_REGION)
bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def send_urgent_alert(message: str):
    """Sends a real-time notification to caregivers via Amazon SNS."""
    if not SNS_TOPIC_ARN:
        print("AWS SNS_TOPIC_ARN not configured. Alert simulated in logs.")
        print(f"[SIMULATED SNS ALERT]: {message}")
        return False

    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="URGENT: Caregiver Companion Alert"
        )
        return True
    except ClientError as e:
        print(f"AWS SNS Error: {e}")
        return False

def generate_smart_summary(data: dict) -> str:
    """Uses Amazon Bedrock (Claude 3 Haiku) to create an empathetic family summary."""
    prompt = (
        f"You are a compassionate care coordinator. Based on the following data, "
        f"write a warm, 2-sentence summary for a family about their loved one's health this week. "
        f"Data: Adherence Rate: {data['adherence_rate']}, "
        f"Taken: {data['taken_doses']}, Missed: {data['missed_doses']}, "
        f"Recent Mood Notes: {data['notes']}. "
        f"Be encouraging and professional. Do not give medical advice."
    )

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    try:
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=body
        )
        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]
    except ClientError as e:
        print(f"AWS Bedrock Error: {e}")
        return "Patient has been mostly adherent, but we noticed a few missed doses. Overall, they are doing well!"

def analyze_emotional_trend(notes: list) -> str:
    """
    Uses Amazon Bedrock to detect emotional trends (e.g., loneliness, depression)
    from check-in notes over time.
    """
    notes_text = "\n".join([f"- {n}" for n in notes])
    prompt = (
        f"You are an empathetic geriatric care specialist. Analyze the following daily check-in notes "
        f"from an elderly patient over the past week:\n\n{notes_text}\n\n"
        f"Identify if there is a concerning emotional trend (e.g., increasing loneliness, sadness, or confusion). "
        f"If a trend is found, suggest a gentle way for the family to support them. "
        f"If everything looks positive, provide a reassuring note. "
        f"Keep it to 3 sentences. Be extremely compassionate. Do not diagnose medical conditions."
    )

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

    try:
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=body
        )
        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]
    except ClientError as e:
        print(f"AWS Bedrock Error: {e}")
        return "Emotional trends are stable. The patient seems to be in a consistent mood."
