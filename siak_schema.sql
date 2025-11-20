-- Faculties Table
CREATE TABLE IF NOT EXISTS faculties (
    faculty_id UUID PRIMARY KEY NOT NULL,
    faculty_code VARCHAR(10) UNIQUE NOT NULL,
    faculty_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- Programs Table
CREATE TABLE IF NOT EXISTS programs (
    program_id UUID PRIMARY KEY NOT NULL,
    program_code VARCHAR(10) UNIQUE NOT NULL,
    program_name VARCHAR(100) NOT NULL,
    faculty_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id)
);
-- Students Table
CREATE TABLE IF NOT EXISTS students (
    student_id UUID PRIMARY KEY NOT NULL,
    npm VARCHAR(10) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    enrollment_date DATE NOT NULL,
    program_id UUID NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
-- Lecturers Table
CREATE TABLE IF NOT EXISTS lecturers (
    lecturer_id UUID PRIMARY KEY NOT NULL,
    nip VARCHAR(18) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    faculty_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (faculty_id) REFERENCES faculties(faculty_id)
);
-- Rooms Table
CREATE TABLE IF NOT EXISTS rooms (
    room_id UUID PRIMARY KEY NOT NULL,
    room_code VARCHAR(20) NOT NULL,
    building VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
-- Courses Table
CREATE TABLE IF NOT EXISTS courses (
    course_id UUID PRIMARY KEY NOT NULL,
    course_code VARCHAR(10) UNIQUE NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INTEGER NOT NULL,
    program_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
-- Semesters Table (is_active removed)
CREATE TABLE IF NOT EXISTS semesters (
    semester_id UUID PRIMARY KEY NOT NULL,
    semester_code VARCHAR(10) UNIQUE NOT NULL,
    semester_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date DATE NOT NULL
);
-- Class Schedules Table
CREATE TABLE IF NOT EXISTS class_schedules (
    schedule_id UUID PRIMARY KEY NOT NULL,
    course_id UUID NOT NULL,
    lecturer_id UUID NOT NULL,
    room_id UUID NOT NULL,
    semester_id UUID NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    start_time_delta TIMESTAMP NOT NULL,
    end_time_delta TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    FOREIGN KEY (semester_id) REFERENCES semesters(semester_id)
);
-- course_Registrations Table
CREATE TABLE IF NOT EXISTS course_registrations (
    registration_id UUID PRIMARY KEY NOT NULL,
    student_id UUID NOT NULL,
    course_id UUID NOT NULL,
    semester_id UUID NOT NULL,
    registration_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (semester_id) REFERENCES semesters(semester_id),
    UNIQUE (student_id, course_id, semester_id)
);
-- Grades Table
CREATE TABLE IF NOT EXISTS grades (
    grade_id UUID PRIMARY KEY NOT NULL,
    registration_id UUID NOT NULL,
    final_grade DECIMAL(5, 2),
    letter_grade VARCHAR(2),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (registration_id) REFERENCES course_registrations(registration_id)
);
-- Semester Fees Table (payment_status removed)
CREATE TABLE IF NOT EXISTS semester_fees (
    fee_id UUID PRIMARY KEY NOT NULL,
    student_id UUID NOT NULL,
    semester_id UUID NOT NULL,
    fee_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (semester_id) REFERENCES semesters(semester_id),
    UNIQUE (student_id, semester_id)
);
-- Academic Records Table (for tracking IP and IPK)
CREATE TABLE IF NOT EXISTS academic_records (
    record_id UUID PRIMARY KEY NOT NULL,
    student_id UUID NOT NULL,
    semester_id UUID NOT NULL,
    semester_gpa DECIMAL(3, 2) NOT NULL,
    -- IP (Indeks Prestasi)
    cumulative_gpa DECIMAL(3, 2) NOT NULL,
    -- IPK (Indeks Prestasi Kumulatif)
    semester_credits INTEGER NOT NULL,
    -- Credits taken this semester
    credits_passed INTEGER NOT NULL,
    -- Credits passed/completed this semester
    total_credits INTEGER NOT NULL,
    -- Total credits earned so far
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (semester_id) REFERENCES semesters(semester_id),
    UNIQUE (student_id, semester_id)
);
