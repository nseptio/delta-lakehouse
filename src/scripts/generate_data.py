import argparse
import json
import logging
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Dict, List

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker
from pyarrow import csv

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
    fake = Faker("id_ID")
    cfg = FakerConfig()

    logger.info("Generating faculties")
    faculties = generate_faculty(fake, cfg.faculty)

    logger.info("Generating programs")
    programs = generate_program(fake, faculties, cfg.program)

    logger.info("Generating lecturers")
    lecturers = generate_lecturer(fake, faculties, cfg.lecturer)

    logger.info("Generating students")
    students = generate_student(fake, programs, cfg.student)

    logger.info("Generating rooms")
    rooms = generate_room(cfg.room)

    logger.info("Generating courses")
    courses = generate_course(fake, programs, cfg.course)

    logger.info("Generating semesters")
    semesters = generate_semester(cfg.semester)

    logger.info("Generating class schedules")
    class_schedules = generate_class_schedule(
        courses, lecturers, rooms, semesters, cfg.class_schedule
    )

    logger.info("Generating registrations")
    cores = os.cpu_count()
    lengths = [len(c) for c in np.array_split(np.zeros(cfg.registration), cores)]
    chunks = [(students, courses, semesters, length) for length in lengths]
    registrations = []
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(generate_registration, s, c, sem, length)
            for s, c, sem, length in chunks
        ]

        for f in as_completed(futures):
            registrations.extend(f.result())

    logger.info("Generating grades")
    grades = generate_grade(registrations)

    logger.info("Generating semester fees")
    semester_fees = generate_semester_fees(students, semesters, programs)

    logger.info("Generating academic records")
    student_chunks = np.array_split(students, cores)
    chunks = [
        (chunk, semesters, registrations, grades, courses) for chunk in student_chunks
    ]
    academic_records = []
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(generate_academic_record, s, sem, reg, g, c)
            for s, sem, reg, g, c in chunks
        ]

        for f in as_completed(futures):
            academic_records.extend(f.result())

    def save(data_name_tuple):
        data, name = data_name_tuple
        if save_format == "csv":
            save_to_csv(data, output_dir, name)
        elif save_format == "parquet":
            save_to_parquet(data, output_dir, name)
        else:
            save_to_json(data, output_dir, name)

    # Save all generated data at the end
    with ThreadPoolExecutor() as executor:
        list(
            executor.map(
                save,
                [
                    (faculties, "faculties"),
                    (programs, "programs"),
                    (lecturers, "lecturers"),
                    (students, "students"),
                    (rooms, "rooms"),
                    (courses, "courses"),
                    (semesters, "semesters"),
                    (class_schedules, "class_schedules"),
                    (registrations, "registrations"),
                    (grades, "grades"),
                    (semester_fees, "semester_fees"),
                    (academic_records, "academic_records"),
                ],
            )
        )


def save_to_json(data: List[Dict], output_dir: str, file_name: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{file_name}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Saved {len(data)} records to {filepath}")


def save_to_csv(data: List[Dict], output_dir: str, file_name: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"{file_name}.csv")
    table = pa.Table.from_pylist(data)
    csv.write_csv(table, filepath)
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
