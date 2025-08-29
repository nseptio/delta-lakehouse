from pyiceberg.schema import NestedField, Schema
from pyiceberg.types import (
    BooleanType,
    DateType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    StringType,
)

# Dimension Tables
dim_student = Schema(
    NestedField(1, "student_id", LongType(), required=True),
    NestedField(2, "npm", StringType(), required=True),
    NestedField(3, "name", StringType(), required=True),
    NestedField(4, "email", StringType(), required=True),
    NestedField(5, "enrollment_date", DateType(), required=True),
    NestedField(6, "is_active", BooleanType(), required=True),
    NestedField(7, "program_code", StringType(), required=True),
    NestedField(8, "program_name", StringType(), required=True),
    NestedField(9, "faculty_code", StringType(), required=True),
    NestedField(10, "faculty_name", StringType(), required=True),
)

dim_course = Schema(
    NestedField(1, "course_id", LongType(), required=True),
    NestedField(2, "course_code", StringType(), required=True),
    NestedField(3, "course_name", StringType(), required=True),
    NestedField(4, "credits", IntegerType(), required=True),
    NestedField(5, "program_code", StringType(), required=True),
    NestedField(6, "program_name", StringType(), required=True),
    NestedField(7, "faculty_code", StringType(), required=True),
    NestedField(8, "faculty_name", StringType(), required=True),
)

dim_lecturer = Schema(
    NestedField(1, "lecturer_id", LongType(), required=True),
    NestedField(2, "nip", StringType(), required=True),
    NestedField(3, "name", StringType(), required=True),
    NestedField(4, "email", StringType(), required=True),
    NestedField(5, "faculty_code", StringType(), required=True),
    NestedField(6, "faculty_name", StringType(), required=True),
)

dim_semester = Schema(
    NestedField(1, "semester_id", IntegerType(), required=True),
    NestedField(2, "semester_code", StringType(), required=True),
    NestedField(3, "start_date", DateType(), required=True),
    NestedField(4, "end_date", DateType(), required=True),
    NestedField(5, "academic_year", StringType(), required=True),
)

dim_class = Schema(
    NestedField(1, "class_id", LongType(), required=True),
    NestedField(2, "class_code", StringType(), required=True),
    NestedField(3, "course_code", StringType(), required=True),
    NestedField(4, "course_name", StringType(), required=True),
    NestedField(5, "lecturer_name", StringType(), required=True),
    NestedField(6, "day_of_week", StringType(), required=True),
    NestedField(7, "start_time", StringType(), required=True),
    NestedField(8, "end_time", StringType(), required=True),
    NestedField(9, "semester_code", StringType(), required=True),
    NestedField(10, "academic_year", StringType(), required=True),
)

dim_room = Schema(
    NestedField(1, "room_id", LongType(), required=True),
    NestedField(2, "building", StringType(), required=True),
    NestedField(3, "capacity", IntegerType(), required=True),
)

# Fact Tables
fact_registration = Schema(
    NestedField(1, "registration_id", LongType(), required=True),
    NestedField(2, "student_id", LongType(), required=True),
    NestedField(3, "course_id", LongType(), required=True),
    NestedField(4, "semester_id", LongType(), required=True),
    NestedField(5, "registration_date", DateType(), required=True),
)

fact_grade = Schema(
    NestedField(1, "grade_id", LongType(), required=True),
    NestedField(2, "student_id", LongType(), required=True),
    NestedField(3, "course_id", LongType(), required=True),
    NestedField(4, "semester_id", LongType(), required=True),
    NestedField(5, "final_grade", FloatType(), required=True),
    NestedField(6, "letter_grade", StringType(), required=True),
)

fact_fee = Schema(
    NestedField(1, "fee_id", LongType(), required=True),
    NestedField(2, "student_id", LongType(), required=True),
    NestedField(3, "semester_id", LongType(), required=True),
    NestedField(4, "fee_amount", DoubleType(), required=True),
    NestedField(5, "payment_date", DateType(), required=False),
)

fact_academic = Schema(
    NestedField(1, "academic_id", LongType(), required=True),
    NestedField(2, "student_id", LongType(), required=True),
    NestedField(3, "semester_id", LongType(), required=True),
    NestedField(4, "semester_gpa", FloatType(), required=True),
    NestedField(5, "cumulative_gpa", FloatType(), required=True),
    NestedField(6, "semester_credits", IntegerType(), required=True),
    NestedField(7, "credits_passed", IntegerType(), required=True),
    NestedField(8, "total_credits", IntegerType(), required=True),
)

fact_teaching = Schema(
    NestedField(1, "teaching_id", LongType(), required=True),
    NestedField(2, "lecturer_id", LongType(), required=True),
    NestedField(3, "course_id", LongType(), required=True),
    NestedField(4, "semester_id", LongType(), required=True),
    NestedField(5, "class_id", LongType(), required=True),
    NestedField(6, "room_id", LongType(), required=True),
    NestedField(7, "total_students", IntegerType(), required=True),
    NestedField(8, "total_sessions", IntegerType(), required=True),
    NestedField(9, "sessions_completed", IntegerType(), required=True),
    NestedField(10, "teaching_hours", IntegerType(), required=True),
)

fact_room_usage = Schema(
    NestedField(1, "usage_id", LongType(), required=True),
    NestedField(2, "room_id", LongType(), required=True),
    NestedField(3, "class_id", LongType(), required=True),
    NestedField(4, "semester_id", LongType(), required=True),
    NestedField(5, "usage_date", DateType(), required=True),
    NestedField(6, "start_time", StringType(), required=True),
    NestedField(7, "end_time", StringType(), required=True),
    NestedField(8, "actual_occupancy", IntegerType(), required=True),
    NestedField(9, "utilization_rate", FloatType(), required=True),
)


SCHEMAS = {
    "dim_student": dim_student,
    "dim_course": dim_course,
    "dim_lecturer": dim_lecturer,
    "dim_semester": dim_semester,
    "dim_class": dim_class,
    "dim_room": dim_room,
    "fact_registration": fact_registration,
    "fact_grade": fact_grade,
    "fact_fee": fact_fee,
    "fact_academic": fact_academic,
    "fact_teaching": fact_teaching,
    "fact_room_usage": fact_room_usage,
}


def get_schema(table_name: str) -> Schema:
    if table_name not in SCHEMAS:
        raise
    return SCHEMAS[table_name]


def list_schemas() -> dict:
    return SCHEMAS.copy()


if __name__ == "__main__":
    pass
