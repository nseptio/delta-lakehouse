import argparse
import json
import logging
import os
from typing import Dict, List

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from src.generator.academic_record_faker import generate_academic_record
from src.generator.class_schedule_faker import generate_class_schedule
from src.generator.course_faker import generate_course
from src.generator.faculty_faker import generate_faculty
from src.generator.grade_faker import generate_grade
from src.generator.lecturer_faker import generate_lecturer
from src.generator.program_faker import generate_program
from src.generator.registration_faker import generate_registration
from src.generator.room_faker import generate_room
from src.generator.semester_faker import generate_semester
from src.generator.semester_fees_faker import generate_semester_fees
from src.generator.student_faker import generate_student
from src.utils.config import FakerConfig
from src.utils.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def save_generated_data(save_format: str, output_dir: str) -> None:
    cfg = FakerConfig()

    def save(data, name):
        if save_format == "csv":
            save_to_csv(data, output_dir, name)
        elif save_format == "parquet":
            save_to_parquet(data, output_dir, name)
        else:
            save_to_json(data, output_dir, name)

    logger.info("Generating faculties")
    faculties = generate_faculty(cfg.faculty)
    save(faculties, "faculties")

    logger.info("Generating programs")
    programs = generate_program(faculties, cfg.program)
    save(programs, "programs")

    logger.info("Generating lecturers")
    lecturers = generate_lecturer(faculties, cfg.lecturer)
    save(lecturers, "lecturers")

    logger.info("Generating students")
    students = generate_student(programs, cfg.student)
    save(students, "students")

    logger.info("Generating rooms")
    rooms = generate_room(cfg.room)
    save(rooms, "rooms")

    logger.info("Generating courses")
    courses = generate_course(programs, cfg.course)
    save(courses, "courses")

    logger.info("Generating semesters")
    semesters = generate_semester(cfg.semester)
    save(semesters, "semesters")

    logger.info("Generating class schedules")
    class_schedules = generate_class_schedule(
        courses, lecturers, rooms, semesters, cfg.class_schedule
    )
    save(class_schedules, "class_schedules")

    logger.info("Generating registrations")
    registrations = generate_registration(
        students, courses, semesters, cfg.registration
    )
    save(registrations, "registrations")

    logger.info("Generating grades")
    grades = generate_grade(registrations)
    save(grades, "grades")

    logger.info("Generating semester fees")
    semester_fees = generate_semester_fees(students, semesters, programs)
    save(semester_fees, "semester_fees")

    logger.info("Generating academic records")
    academic_records = generate_academic_record(
        students, semesters, registrations, grades, courses
    )
    save(academic_records, "academic_records")


def save_to_json(data: List[Dict], output_dir: str, file_name: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{file_name}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved {len(data)} records to {filepath}")


def save_to_csv(data: List[Dict], output_dir: str, file_name: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"{file_name}.csv")
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    logger.info(f"Saved {len(data)} records to {filepath}")


def save_to_parquet(data: List[Dict], output_dir: str, file_name: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"{file_name}.parquet")
    table = pa.Table.from_pylist(data)
    pq.write_table(table, filepath)
    logger.info(f"Saved {len(data)} records to {filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fake academic data")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "parquet"],
        default="parquet",
        help="Output format for generated data (default: parquet)",
    )
    parser.add_argument(
        "--output_dir",
        default="data/generated",
        help="Directory to save generated data (default: data/generated)",
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    save_generated_data(args.format, args.output_dir)
