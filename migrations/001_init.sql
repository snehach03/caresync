--Database Initialization
-- Caregiver Companion Schema
-- Using TIMESTAMPTZ for all time fields to handle timezones correctly

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    role TEXT CHECK (role IN ('patient', 'caregiver')),
    timezone TEXT NOT NULL DEFAULT 'UTC',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE care_relationships (
    patient_id UUID REFERENCES users(id) ON DELETE CASCADE,
    caregiver_id UUID REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (patient_id, caregiver_id)
);

CREATE TABLE medications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    frequency TEXT,
    instructions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    medication_id UUID REFERENCES medications(id) ON DELETE CASCADE,
    scheduled_time TIME NOT NULL, -- Local time of day
    day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sunday
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dose_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    schedule_id UUID REFERENCES schedules(id) ON DELETE CASCADE,
    taken_at TIMESTAMPTZ NOT NULL,
    status TEXT CHECK (status IN ('taken', 'missed', 'skipped')),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE checkins (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES users(id) ON DELETE CASCADE,
    mood_score INTEGER CHECK (mood_score BETWEEN 1 AND 5),
    notes TEXT,
    recorded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    location TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    caregiver_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type TEXT CHECK (type IN ('missed_dose', 'health_warning')),
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_dose_logs_schedule ON dose_logs(schedule_id);
CREATE INDEX idx_schedules_med ON schedules(medication_id);
CREATE INDEX idx_checkins_patient ON checkins(patient_id);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_alerts_caregiver ON alerts(caregiver_id);
