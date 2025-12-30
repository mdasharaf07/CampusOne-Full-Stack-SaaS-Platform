-- ==========================================
-- CampusHub Extracted Database Schema
-- Extracted on: '1970-01-01T05:30:00+05:30'::timestamptz
-- ==========================================

-- Table: attendance
CREATE TABLE IF NOT EXISTS attendance (
id SERIAL NOT NULL,
event_id INTEGER,
student_id INTEGER,
manual_present BOOLEAN  DEFAULT false,
otp_present BOOLEAN  DEFAULT false,
event_otp VARCHAR,
otp_sent_at TIMESTAMP WITHOUT TIME ZONE,
otp_verified_at TIMESTAMP WITHOUT TIME ZONE,
marked_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (event_id),
    UNIQUE (student_id)
);

-- Table: certificates
CREATE TABLE IF NOT EXISTS certificates (
id SERIAL NOT NULL,
event_id INTEGER,
student_id INTEGER,
file_url TEXT NOT NULL,
uploaded_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (event_id),
    UNIQUE (student_id)
);

-- Table: clubs
CREATE TABLE IF NOT EXISTS clubs (
id SERIAL NOT NULL,
category VARCHAR NOT NULL,
name VARCHAR NOT NULL,
razorpay_key_id VARCHAR,
razorpay_key_secret VARCHAR,
master_gsheet_link TEXT,
    PRIMARY KEY (id),
    UNIQUE (name)
);

-- Table: cultural_bookings
CREATE TABLE IF NOT EXISTS cultural_bookings (
id SERIAL NOT NULL,
cultural_id INTEGER,
student_id INTEGER,
status TEXT  DEFAULT 'pending'::text,
razorpay_order_id TEXT,
razorpay_payment_id TEXT,
razorpay_signature TEXT,
ticket_id VARCHAR,
amount_paid NUMERIC,
booked_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
payment_initiated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY (cultural_id) REFERENCES culturals(id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (cultural_id),
    UNIQUE (student_id)
);

-- Table: culturals
CREATE TABLE IF NOT EXISTS culturals (
id SERIAL NOT NULL,
title TEXT NOT NULL,
description TEXT,
price NUMERIC  DEFAULT 0,
total_tickets INTEGER NOT NULL,
available_tickets INTEGER NOT NULL,
event_date TIMESTAMP WITHOUT TIME ZONE,
venue TEXT,
template_id VARCHAR  DEFAULT 'classic_purple'::character varying,
club_id INTEGER,
created_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
booking_deadline TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL
);

-- Table: events
CREATE TABLE IF NOT EXISTS events (
id SERIAL NOT NULL,
title VARCHAR NOT NULL,
description TEXT,
start_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
end_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
reg_deadline TIMESTAMP WITHOUT TIME ZONE NOT NULL,
reg_amount NUMERIC  DEFAULT 0.00,
min_team_size INTEGER  DEFAULT 1,
team_size INTEGER  DEFAULT 1,
female_mandatory BOOLEAN  DEFAULT false,
poster_url TEXT,
organizer_id INTEGER,
club_id INTEGER,
status VARCHAR  DEFAULT 'pending'::character varying,
admin_message TEXT,
approved_by INTEGER,
event_flow JSONB,
refreshments JSONB,
hall_id INTEGER,
attendance_code VARCHAR,
cert_folder_url TEXT,
created_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
attendance_locked BOOLEAN  DEFAULT false,
    PRIMARY KEY (id),
    FOREIGN KEY (organizer_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (hall_id) REFERENCES halls(id) ON DELETE SET NULL
);

-- Table: friends
CREATE TABLE IF NOT EXISTS friends (
id SERIAL NOT NULL,
user_id INTEGER,
friend_id INTEGER,
status VARCHAR  DEFAULT 'pending'::character varying,
created_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (friend_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (user_id),
    UNIQUE (friend_id)
);

-- Table: halls
CREATE TABLE IF NOT EXISTS halls (
id SERIAL NOT NULL,
name VARCHAR NOT NULL,
capacity INTEGER NOT NULL,
description TEXT,
    PRIMARY KEY (id),
    UNIQUE (name)
);

-- Table: otp_verifications
CREATE TABLE IF NOT EXISTS otp_verifications (
id SERIAL NOT NULL,
email VARCHAR NOT NULL,
role VARCHAR NOT NULL,
otp_code VARCHAR NOT NULL,
payload TEXT NOT NULL,
expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
created_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (role)
);

-- Table: refresh_tokens
CREATE TABLE IF NOT EXISTS refresh_tokens (
id SERIAL NOT NULL,
user_id INTEGER,
token_hash VARCHAR NOT NULL,
device_id VARCHAR,
ip_address VARCHAR,
user_agent TEXT,
expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
created_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (token_hash)
);

-- Table: registration_members
CREATE TABLE IF NOT EXISTS registration_members (
id SERIAL NOT NULL,
registration_id INTEGER,
student_id INTEGER,
invite_status VARCHAR  DEFAULT 'accepted'::character varying,
invite_expires_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY (registration_id) REFERENCES registrations(id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (registration_id),
    UNIQUE (student_id)
);

-- Table: registrations
CREATE TABLE IF NOT EXISTS registrations (
id SERIAL NOT NULL,
event_id INTEGER,
student_id INTEGER,
payment_proof_url TEXT,
razorpay_order_id VARCHAR,
razorpay_payment_id VARCHAR,
razorpay_signature VARCHAR,
amount_paid NUMERIC,
invoice_url TEXT,
status VARCHAR  DEFAULT 'pending'::character varying,
registered_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
team_name TEXT,
leader_id INTEGER,
payer_id INTEGER,
edit_count INTEGER  DEFAULT 0,
payment_initiated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (leader_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (payer_id) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (event_id),
    UNIQUE (student_id)
);

-- Table: revoked_tokens
CREATE TABLE IF NOT EXISTS revoked_tokens (
jti VARCHAR NOT NULL,
expires_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (jti)
);

-- Table: user_session_history
CREATE TABLE IF NOT EXISTS user_session_history (
id SERIAL NOT NULL,
user_id INTEGER,
action VARCHAR NOT NULL,
ip_address VARCHAR,
user_agent TEXT,
timestamp TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

-- Table: users
CREATE TABLE IF NOT EXISTS users (
id SERIAL NOT NULL,
full_name VARCHAR NOT NULL,
email VARCHAR NOT NULL,
reg_no VARCHAR,
password_hash VARCHAR NOT NULL,
phone_number TEXT,
address TEXT,
dob TEXT,
role VARCHAR NOT NULL,
account_status VARCHAR  DEFAULT 'active'::character varying,
department TEXT,
college_email TEXT,
gender VARCHAR,
organization_name TEXT,
club_id INTEGER,
created_at TIMESTAMP WITHOUT TIME ZONE  DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE SET NULL,
    UNIQUE (email),
    UNIQUE (role),
    UNIQUE (reg_no)
);

-- Function: set_event_club_id
CREATE OR REPLACE FUNCTION public.set_event_club_id()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.club_id IS NULL THEN
        SELECT club_id INTO NEW.club_id FROM users WHERE id = NEW.organizer_id;
    END IF;
    RETURN NEW;
END;
$function$;

-- Trigger: trg_set_event_club_id
CREATE TRIGGER trg_set_event_club_id BEFORE INSERT ON public.events FOR EACH ROW EXECUTE FUNCTION set_event_club_id();

-- SEED DATA
INSERT INTO clubs (category, name) VALUES 
('Technical & Research Teams', 'SRMKZILLA'),
('Technical & Research Teams', 'Google Developer Student Club (GDSC)'),
('Technical & Research Teams', 'Next Tech Lab'),
('Technical & Research Teams', 'Data Science Community SRM'),
('Technical & Research Teams', 'IoT Alliance Club'),
('Technical & Research Teams', 'SRM Rudra'),
('Technical & Research Teams', 'Camber Racing'),
('Technical & Research Teams', '4ZE Racing'),
('Technical & Research Teams', 'SRM UAV'),
('Technical & Research Teams', 'Quantum Computing Club'),
('Technical & Research Teams', 'Infi-alpha-Hyperloop'),
('Cultural & Creative Clubs', 'Dance Club'),
('Cultural & Creative Clubs', 'Music Club'),
('Cultural & Creative Clubs', 'Literary Club'),
('Cultural & Creative Clubs', 'Movies and Dramatics Club'),
('Cultural & Creative Clubs', 'Photography Club'),
('Cultural & Creative Clubs', 'Fashion Club'),
('Cultural & Creative Clubs', 'Astrophilia'),
('Cultural & Creative Clubs', 'Fine Arts Club'),
('Professional Chapters & Societies', 'ACM'),
('Professional Chapters & Societies', 'IEEE'),
('Professional Chapters & Societies', 'CSI'),
('Professional Chapters & Societies', 'IEI'),
('Professional Chapters & Societies', 'SAE'),
('Professional Chapters & Societies', 'IET'),
('Social & Special Interest Clubs', 'Rotaract Club of SRM KTR'),
('Social & Special Interest Clubs', 'E-Cell (Entrepreneurship Cell)'),
('Social & Special Interest Clubs', 'The Listening Space'),
('Social & Special Interest Clubs', 'SRM MUN'),
('Social & Special Interest Clubs', 'NSS (National Service Scheme)'),
('Department-Specific Clubs', 'Pie Club'),
('Department-Specific Clubs', 'Tekmedica'),
('Department-Specific Clubs', 'BIS Standards Club'),
('Department-Specific Clubs', 'Finance & Media Clubs'),
('Major Fest Committees', 'Aaruush'),
('Major Fest Committees', 'Milan')
ON CONFLICT (name) DO NOTHING;

INSERT INTO halls (name, capacity, description) VALUES 
('SRM TP 404 & 405', 120, 'Combined large classroom in TP building'),
('SRM GANESAN AUDITORIUM', 500, 'Large auditorium for main events'),
('MEDICAL HALL', 200, 'Hall near the medical block'),
('BELL LAB 502', 40, 'Laboratory/Seminar Room')
ON CONFLICT (name) DO NOTHING;
