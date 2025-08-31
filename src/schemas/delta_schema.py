import pyarrow as pa

dim_student = pa.schema(
    [
        pa.field("student_id", pa.int64(), nullable=False),
        pa.field("npm", pa.string(), nullable=False),
        pa.field("name", pa.string(), nullable=False),
        pa.field("email", pa.string(), nullable=False),
        pa.field("enrollment_date", pa.date32(), nullable=False),
        pa.field("is_active", pa.bool_(), nullable=False),
        pa.field("program_code", pa.string(), nullable=False),
        pa.field("program_name", pa.string(), nullable=False),
        pa.field("faculty_code", pa.string(), nullable=False),
        pa.field("faculty_name", pa.string(), nullable=False),
    ]
)

dim_course = pa.schema(
    [
        pa.field("course_id", pa.int64(), nullable=False),
        pa.field("course_code", pa.string(), nullable=False),
        pa.field("course_name", pa.string(), nullable=False),
        pa.field("credits", pa.int32(), nullable=False),
        pa.field("program_code", pa.string(), nullable=False),
        pa.field("program_name", pa.string(), nullable=False),
        pa.field("faculty_code", pa.string(), nullable=False),
        pa.field("faculty_name", pa.string(), nullable=False),
    ]
)

dim_lecturer = pa.schema(
    [
        pa.field("lecturer_id", pa.int64(), nullable=False),
        pa.field("nip", pa.string(), nullable=False),
        pa.field("name", pa.string(), nullable=False),
        pa.field("email", pa.string(), nullable=False),
        pa.field("faculty_code", pa.string(), nullable=False),
        pa.field("faculty_name", pa.string(), nullable=False),
    ]
)

dim_semester = pa.schema(
    [
        pa.field("semester_id", pa.int32(), nullable=False),
        pa.field("semester_code", pa.string(), nullable=False),
        pa.field("start_date", pa.date32(), nullable=False),
        pa.field("end_date", pa.date32(), nullable=False),
        pa.field("academic_year", pa.string(), nullable=False),
    ]
)

dim_class = pa.schema(
    [
        pa.field("class_id", pa.int64(), nullable=False),
        pa.field("class_code", pa.string(), nullable=False),
        pa.field("course_code", pa.string(), nullable=False),
        pa.field("course_name", pa.string(), nullable=False),
        pa.field("lecturer_name", pa.string(), nullable=False),
        pa.field("day_of_week", pa.string(), nullable=False),
        pa.field("start_time", pa.string(), nullable=False),
        pa.field("end_time", pa.string(), nullable=False),
        pa.field("semester_code", pa.string(), nullable=False),
        pa.field("academic_year", pa.string(), nullable=False),
    ]
)

dim_room = pa.schema(
    [
        pa.field("room_id", pa.int64(), nullable=False),
        pa.field("building", pa.string(), nullable=False),
        pa.field("capacity", pa.int32(), nullable=False),
    ]
)

################################################################################
# FACT TABLES
################################################################################

fact_registration = pa.schema(
    [
        pa.field("registration_id", pa.int64(), nullable=False),
        pa.field("student_id", pa.int64(), nullable=False),
        pa.field("course_id", pa.int64(), nullable=False),
        pa.field("semester_id", pa.int64(), nullable=False),
        pa.field("registration_date", pa.date32(), nullable=False),
    ]
)

fact_grade = pa.schema(
    [
        pa.field("grade_id", pa.int64(), nullable=False),
        pa.field("student_id", pa.int64(), nullable=False),
        pa.field("course_id", pa.int64(), nullable=False),
        pa.field("semester_id", pa.int64(), nullable=False),
        pa.field("final_grade", pa.float32(), nullable=False),
        pa.field("letter_grade", pa.string(), nullable=False),
    ]
)

fact_fee = pa.schema(
    [
        pa.field("fee_id", pa.int64(), nullable=False),
        pa.field("student_id", pa.int64(), nullable=False),
        pa.field("semester_id", pa.int64(), nullable=False),
        pa.field("fee_amount", pa.float64(), nullable=False),
        pa.field("payment_date", pa.date32()),
    ]
)

fact_academic = pa.schema(
    [
        pa.field("academic_id", pa.int64(), nullable=False),
        pa.field("student_id", pa.int64(), nullable=False),
        pa.field("semester_id", pa.int64(), nullable=False),
        pa.field("semester_gpa", pa.float32(), nullable=False),
        pa.field("cumulative_gpa", pa.float32(), nullable=False),
        pa.field("semester_credits", pa.int32(), nullable=False),
        pa.field("credits_passed", pa.int32(), nullable=False),
        pa.field("total_credits", pa.int32(), nullable=False),
    ]
)

# fact_attendence = pa.schema(
#     [
#         pa.field("attendence_id", pa.int64(), nullable=False),
#         pa.field("student_id", pa.int64(), nullable=False),
#         pa.field("course_id", pa.int64(), nullable=False),
#         pa.field("class_id", pa.int64(), nullable=False),
#         pa.field("room_id", pa.int64(), nullable=False),
#         pa.field("attendence_date", pa.date32(), nullable=False),
#         pa.field("check_in_time", pa.string(), nullable=False),
#     ]
# )

fact_teaching = pa.schema(
    [
        pa.field("teaching_id", pa.int64(), nullable=False),
        pa.field("lecturer_id", pa.int64(), nullable=False),
        pa.field("course_id", pa.int64(), nullable=False),
        pa.field("semester_id", pa.int64(), nullable=False),
        pa.field("class_id", pa.int64(), nullable=False),
        pa.field("room_id", pa.int64(), nullable=False),
        pa.field("total_students", pa.int32(), nullable=False),
        pa.field("total_sessions", pa.int32(), nullable=False),
        pa.field("sessions_completed", pa.int32(), nullable=False),
        pa.field("teaching_hours", pa.int32(), nullable=False),
    ]
)

fact_room_usage = pa.schema(
    [
        pa.field("usage_id", pa.int64(), nullable=False),
        pa.field("room_id", pa.int64(), nullable=False),
        pa.field("class_id", pa.int64(), nullable=False),
        pa.field("semester_id", pa.int64(), nullable=False),
        pa.field("usage_date", pa.date32(), nullable=False),
        pa.field("start_time", pa.string(), nullable=False),
        pa.field("end_time", pa.string(), nullable=False),
        pa.field("actual_occupancy", pa.int32(), nullable=False),
        pa.field("utilization_rate", pa.float32(), nullable=False),
    ]
)


# Dictionary mapping table names to schemas for easy access
SCHEMAS = {
    # Dimension Tables
    "dim_student": dim_student,
    "dim_course": dim_course,
    "dim_lecturer": dim_lecturer,
    "dim_semester": dim_semester,
    "dim_class": dim_class,
    "dim_room": dim_room,
    # Fact Tables
    "fact_registration": fact_registration,
    "fact_grade": fact_grade,
    "fact_fee": fact_fee,
    "fact_academic": fact_academic,
    # "fact_attendence": fact_attendence,
    "fact_teaching": fact_teaching,
    "fact_room_usage": fact_room_usage,
}


def get_schema(table_name: str) -> pa.Schema:
    """Get schema by table name"""
    if table_name not in SCHEMAS:
        raise ValueError(f"Schema not found for table: {table_name}")
    return SCHEMAS[table_name]


def list_schemas() -> dict:
    """Return all available schemas"""
    return SCHEMAS.copy()


if __name__ == "__main__":
    pass
