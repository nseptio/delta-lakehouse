import logging

from duckdb import DuckDBPyConnection

logger = logging.getLogger(__name__)


def transform_dim_student(duck: DuckDBPyConnection):
    # alter student id column to student_id
    # denormalized students, programs, and faculties tables
    duck.execute("""
        CREATE OR REPLACE TABLE dim_student AS
        SELECT
            s.id AS student_id,
            s.npm,
            s.name,
            s.email,
            s.enrollment_date,
            s.is_active,
            p.program_code,
            p.program_name,
            f.faculty_code,
            f.faculty_name
        FROM students s
        JOIN programs p ON s.program_id = p.id
        JOIN faculties f ON p.faculty_id = f.id
    """)


def transform_dim_course(duck: DuckDBPyConnection):
    # denormalized courses, programs, faculties tables
    # alter courses id column to course_id
    duck.execute("""
        CREATE OR REPLACE TABLE dim_course AS
        SELECT
            c.id AS course_id,
            c.course_code,
            c.course_name,
            c.credits,
            p.program_code,
            p.program_name,
            f.faculty_code,
            f.faculty_name
        FROM courses c
        JOIN programs p ON c.program_id = p.id
        JOIN faculties f ON p.faculty_id = f.id
    """)


def transform_dim_lecturer(duck: DuckDBPyConnection):
    # denormalized lecturer and faculties tables
    duck.execute("""
        CREATE OR REPLACE TABLE dim_lecturer AS
        SELECT
            l.id AS lecturer_id,
            l.nip,
            l.name,
            l.email,
            f.faculty_code,
            f.faculty_name
        FROM lecturers l
        JOIN faculties f ON l.faculty_id = f.id
    """)


def transform_dim_semester(duck: DuckDBPyConnection):
    # Keep DATE fields as DATE type for proper PyArrow date32 compatibility
    duck.execute("""
        CREATE OR REPLACE TABLE dim_semester AS
        SELECT
            id AS semester_id,
            semester_code,
            start_date,
            end_date,
            CASE
                WHEN CONTAINS(semester_code, '/') THEN
                    SPLIT_PART(semester_code, '/', 2)
                ELSE
                    CAST(YEAR(start_date) AS VARCHAR) || '/' || CAST(YEAR(end_date) AS VARCHAR)
            END AS academic_year
        FROM semesters
    """)


def transform_dim_room(duck: DuckDBPyConnection):
    # Fixed: Remove room_number field to match schema (3 fields: room_id, building, capacity)
    duck.execute("""
        CREATE OR REPLACE TABLE dim_room AS
        SELECT
            id AS room_id,
            building,
            capacity
        FROM rooms
    """)


def transform_dim_class(duck: DuckDBPyConnection):
    # Keep TIME fields as TIME type for proper PyArrow time32 compatibility
    duck.execute("""
        CREATE OR REPLACE TABLE dim_class AS
        SELECT
            cs.id AS class_id,
            c.course_code || '_' || l.name || '_' || s.semester_code AS class_code,
            c.course_code,
            c.course_name,
            l.name AS lecturer_name,
            cs.day_of_week,
            CAST(cs.start_time AS VARCHAR) AS start_time,
            CAST(cs.end_time AS VARCHAR) AS end_time,
            s.semester_code,
            CASE
                WHEN CONTAINS(s.semester_code, '/') THEN
                    SPLIT_PART(s.semester_code, '/', 2)
                ELSE
                    CAST(YEAR(s.start_date) AS VARCHAR) || '/' || CAST(YEAR(s.end_date) AS VARCHAR)
            END AS academic_year
        FROM class_schedules cs
        JOIN courses c ON cs.course_id = c.id
        JOIN lecturers l ON cs.lecturer_id = l.id
        JOIN semesters s ON cs.semester_id = s.id
    """)


def transform_fact_registration(duck: DuckDBPyConnection):
    duck.execute("""
        CREATE OR REPLACE TABLE fact_registration AS
        SELECT
            r.id AS registration_id,
            r.student_id,
            r.course_id,
            r.semester_id,
            r.registration_date,
        FROM registrations r
    """)


def transform_fact_fee(duck: DuckDBPyConnection):
    # Transform semester_fees to fact_fee
    # alter semester_fees column id to fee_id
    duck.execute("""
        CREATE OR REPLACE TABLE fact_fee AS
        SELECT
            sf.id AS fee_id,
            sf.student_id,
            sf.semester_id,
            sf.fee_amount,
            sf.payment_date::DATE AS payment_date
        FROM semester_fees sf
    """)


def transform_fact_academic(duck: DuckDBPyConnection):
    duck.execute("""
    CREATE OR REPLACE TABLE fact_academic AS
    SELECT
        ac.id AS academic_id,
        ac.student_id,
        ac.semester_id,
        ac.semester_gpa,
        ac.cumulative_gpa,
        ac.semester_credits,
        ac.credits_passed,
        ac.total_credits
    FROM academic_records ac
    """)


def transform_fact_grade(duck: DuckDBPyConnection):
    duck.execute("""
        CREATE OR REPLACE TABLE fact_grade AS
        SELECT
            g.id AS grade_id,
            r.student_id,
            r.course_id,
            r.semester_id,
            g.final_grade,
            g.letter_grade
        FROM grades g
        JOIN registrations r ON g.registration_id = r.id
    """)


# def transform_fact_attendance(duck: DuckDBPyConnection):
#     duck.execute("""
#         CREATE OR REPLACE TABLE fact_attendance AS
#         SELECT
#             !!! THIS ATTENDANCE TABLE SOMEHOW NOT CREATED FROM POSTGRESQL DATABASE
#             !!! I JUST FOLLOWED SOMEONE'S ADV. DATABASE COURSE PROJECT LAST SEMESTER
#             !!! https://github.com/isaui/SIAK-analytics-advanced-database
#     """)


def transform_fact_teaching(duck: DuckDBPyConnection):
    # OK, this doesn't make any sense for me; the same goes for the attendance table
    # The attendance table and this random value for teaching are generated, and don't come from the PostgreSQL db
    # which is not ideal to demonstrate an ETL pipeline
    #
    # But whatever, this flow just followed someone's Adv. Database course project last semester
    # So, just bear with it
    duck.execute("""
        CREATE OR REPLACE TABLE fact_teaching AS
        SELECT
            CAST(cs.id AS BIGINT) AS teaching_id,
            CAST(cs.lecturer_id AS BIGINT) AS lecturer_id,
            CAST(cs.course_id AS BIGINT) AS course_id,
            CAST(cs.semester_id AS BIGINT) AS semester_id,
            CAST(cs.id AS BIGINT) AS class_id,
            CAST(cs.room_id AS BIGINT) AS room_id,
            CAST(FLOOR(RANDOM() * 31) + 15 AS INTEGER) AS total_students,  -- 15-45 students per class
            CAST(FLOOR(RANDOM() * 3) + 14 AS INTEGER) AS total_sessions,   -- 14-16 sessions per semester
            CAST(FLOOR(RANDOM() * 17) AS INTEGER) AS sessions_completed,   -- 0-16 sessions completed
            CAST(ROUND((RANDOM() * 2.0 + 2.0)::DECIMAL, 1) AS INTEGER) AS teaching_hours  -- 2.0-4.0 hours per session
        FROM class_schedules cs
        WHERE cs.id IS NOT NULL AND cs.lecturer_id IS NOT NULL AND cs.course_id IS NOT NULL AND cs.semester_id IS NOT NULL AND cs.room_id IS NOT NULL
    """)


def transform_fact_room_usage(duck: DuckDBPyConnection):
    duck.execute("""
        CREATE OR REPLACE TABLE fact_room_usage AS
        SELECT
            CAST(cs.id AS BIGINT) AS usage_id,
            CAST(cs.room_id AS BIGINT) AS room_id,
            CAST(cs.id AS BIGINT) AS class_id,
            CAST(cs.semester_id AS BIGINT) AS semester_id,
            CAST(CURRENT_DATE - INTERVAL (FLOOR(RANDOM() * 91)::INT) DAY AS DATE) AS usage_date,
            CAST(cs.start_time AS VARCHAR) AS start_time,
            CAST(cs.end_time AS VARCHAR) AS end_time,
            CAST(FLOOR(RANDOM() * 31) + 10 AS INTEGER) AS actual_occupancy,  -- 10-40 students
            CAST(ROUND(((FLOOR(RANDOM() * 31) + 10) / 50.0) * 100, 2) AS FLOAT) AS utilization_rate  -- Utilization rate based on capacity of 50
        FROM class_schedules cs
        WHERE cs.id IS NOT NULL AND cs.room_id IS NOT NULL AND cs.semester_id IS NOT NULL AND cs.start_time IS NOT NULL AND cs.end_time IS NOT NULL
    """)


def transform(duck: DuckDBPyConnection):
    logger.info("🚀 Starting ETL Transform Process")
    # Transform each dimension table
    transform_dim_student(duck)
    transform_dim_course(duck)
    transform_dim_semester(duck)
    transform_dim_class(duck)
    transform_dim_lecturer(duck)
    transform_dim_room(duck)

    # Transform each fact table
    transform_fact_registration(duck)
    transform_fact_fee(duck)
    transform_fact_academic(duck)
    transform_fact_grade(duck)
    transform_fact_teaching(duck)
    transform_fact_room_usage(duck)

    logger.info("✅ ETL Transform Process Completed Successfully")
