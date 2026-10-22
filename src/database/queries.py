from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from .models import Medication, Schedule, DoseLog, Checkin, Appointment, Alert, User
from src.utils.aws_clients import send_urgent_alert, generate_smart_summary, analyze_emotional_trend

def get_todays_medications(db: Session, patient_id: str):
    # This is a simplified version for the demo. In a real app,
    # we would calculate the current day of week and filter schedules.
    meds = db.query(Medication).filter(Medication.patient_id == patient_id, Medication.is_active == True).all()
    results = []
    for med in meds:
        schedules = db.query(Schedule).filter(Schedule.medication_id == med.id).all()
        for s in schedules:
            results.append({
                "medication": med.name,
                "dosage": med.dosage,
                "time": s.scheduled_time.strftime("%H:%M"),
                "schedule_id": str(s.id)
            })
    return results

def log_dose(db: Session, schedule_id: str, status: str = "taken", notes: str = None):
    # Guardrail: Check for duplicate logging within 15 minutes
    fifteen_mins_ago = datetime.now() - timedelta(minutes=15)
    existing = db.query(DoseLog).filter(
        DoseLog.schedule_id == schedule_id,
        DoseLog.taken_at >= fifteen_mins_ago
    ).first()

    if existing:
        raise ValueError("A dose was already logged for this medication in the last 15 minutes.")

    log = DoseLog(schedule_id=schedule_id, taken_at=datetime.now(), status=status, notes=notes)
    db.add(log)
    db.commit()
    return log

def create_missed_dose_alert(db: Session, schedule_id: str, reason: str = "Not reported"):
    # Find the medication and caregiver
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    med = db.query(Medication).filter(Medication.id == schedule.medication_id).first()

    # Log as missed
    log = DoseLog(schedule_id=schedule_id, taken_at=datetime.now(), status="missed", notes=reason)
    db.add(log)

    # Find caregivers associated with this patient
    from .models import User # avoid circular import if needed
    caregivers = db.query(User).filter(User.role == 'caregiver').all() # In reality, use care_relationships

    alert_message = f"Missed Dose Alert: {med.name} was not taken by the patient. Reason: {reason}"

    for cg in caregivers:
        alert = Alert(caregiver_id=cg.id, type="missed_dose",
                      message=alert_message)
        db.add(alert)

        # AWS INTEGRATION: Send real-time SNS notification
        send_urgent_alert(f"Attention {cg.full_name}: {alert_message}")

    db.commit()
    return "Alert sent to caregiver via database and Amazon SNS."

def add_checkin(db: Session, patient_id: str, mood: int, notes: str):
    checkin = Checkin(patient_id=patient_id, mood_score=mood, notes=notes)
    db.add(checkin)
    db.commit()
    return "Check-in recorded successfully."

def get_weekly_summary(db: Session, patient_id: str):
    week_ago = datetime.now() - timedelta(days=7)
    logs = db.query(DoseLog).join(Schedule).join(Medication).filter(
        Medication.patient_id == patient_id,
        DoseLog.taken_at >= week_ago
    ).all()

    total = len(logs)
    taken = len([l for l in logs if l.status == 'taken'])
    adherence = (taken / total * 100) if total > 0 else 0

    # Collect mood notes for the AI
    checkins = db.query(Checkin).filter(
        Checkin.patient_id == patient_id,
        Checkin.recorded_at >= week_ago
    ).all()
    notes_summary = " ".join([c.notes for c in checkins if c.notes])

    # AWS INTEGRATION: Use Bedrock for a "Smart Summary"
    ai_summary = generate_smart_summary({
        "adherence_rate": f"{adherence:.1f}%",
        "taken_doses": taken,
        "missed_doses": total - taken,
        "notes": notes_summary or "No mood notes this week."
    })

    return {
        "adherence_rate": f"{adherence:.1f}%",
        "total_doses": total,
        "taken_doses": taken,
        "missed_doses": total - taken,
        "summary": ai_summary
    }

def get_emotional_trend(db: Session, patient_id: str):
    week_ago = datetime.now() - timedelta(days=7)
    checkins = db.query(Checkin).filter(
        Checkin.patient_id == patient_id,
        Checkin.recorded_at >= week_ago
    ).all()

    notes = [c.notes for c in checkins if c.notes]
    if not notes:
        return "Not enough check-in notes to detect a trend. Please encourage the patient to share more."

    return analyze_emotional_trend(notes)
