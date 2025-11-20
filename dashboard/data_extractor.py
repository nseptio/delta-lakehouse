"""
Data Extractor Module
Handles data extraction from DuckDB database for the university dashboard
"""

import logging
import os
from typing import Dict

import duckdb
import pandas as pd


class DataExtractor:
    """Extracts data from DuckDB database for dashboard visualization"""

    def __init__(self, db_path: str = None):
        """
        Initialize the data extractor

        Args:
            db_path: Path to the DuckDB database file
        """
        if db_path is None:
            # Default path relative to the dashboard directory
            self.db_path = os.path.join(
                os.path.dirname(__file__), "../data/duckdb/siak.duckdb"
            )
        else:
            self.db_path = db_path

        self.connection = None
        self._connect()

    def _connect(self):
        """Establish connection to DuckDB database"""
        try:
            self.connection = duckdb.connect(self.db_path, read_only=True)
            logging.info(f"Connected to DuckDB at {self.db_path}")
        except Exception as e:
            logging.error(f"Failed to connect to DuckDB: {e}")
            raise

    def _execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame

        Args:
            query: SQL query string

        Returns:
            DataFrame with query results
        """
        try:
            result = self.connection.execute(query).fetchdf()
            return result
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            logging.error(f"Query: {query}")
            return pd.DataFrame()

    def _execute_delta_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query on Delta Lake tables and return results as DataFrame

        Args:
            query: SQL query string

        Returns:
            DataFrame with query results
        """
        try:
            # Enable Delta Lake extension
            self.connection.execute("INSTALL delta;")
            self.connection.execute("LOAD delta;")
            result = self.connection.execute(query).fetchdf()
            return result
        except Exception as e:
            logging.error(f"Delta query execution failed: {e}")

    def get_dimension_tables(self) -> Dict[str, pd.DataFrame]:
        """Get all dimension tables"""
        dimension_tables = {}

        # Define dimension table queries
        queries = {
            "dim_student": """
                SELECT * FROM dim_student
                ORDER BY student_id
            """,
            "dim_course": """
                SELECT * FROM dim_course
                ORDER BY course_id
            """,
            "dim_lecturer": """
                SELECT * FROM dim_lecturer
                ORDER BY lecturer_id
            """,
            "dim_semester": """
                SELECT * FROM dim_semester
                ORDER BY semester_id
            """,
            "dim_class": """
                SELECT * FROM dim_class
                ORDER BY class_id
            """,
            "dim_room": """
                SELECT * FROM dim_room
                ORDER BY room_id
            """,
        }

        for table_name, query in queries.items():
            try:
                dimension_tables[table_name] = self._execute_query(query)
                logging.info(
                    f"Loaded {table_name}: {len(dimension_tables[table_name])} rows"
                )
            except Exception as e:
                logging.warning(f"Failed to load {table_name}: {e}")
                dimension_tables[table_name] = pd.DataFrame()

        return dimension_tables

    def get_fact_tables(self) -> Dict[str, pd.DataFrame]:
        """Get all fact tables"""
        fact_tables = {}

        # Define fact table queries
        queries = {
            "fact_registration": """
                SELECT * FROM fact_registration
                ORDER BY registration_id
            """,
            "fact_grade": """
                SELECT * FROM fact_grade
                ORDER BY grade_id
            """,
            "fact_fee": """
                SELECT * FROM fact_fee
                ORDER BY fee_id
            """,
            "fact_academic": """
                SELECT * FROM fact_academic
                ORDER BY academic_id
            """,
            "fact_teaching": """
                SELECT * FROM fact_teaching
                ORDER BY teaching_id
            """,
            "fact_room_usage": """
                SELECT * FROM fact_room_usage
                ORDER BY usage_id
            """,
        }

        for table_name, query in queries.items():
            try:
                fact_tables[table_name] = self._execute_query(query)
                logging.info(
                    f"Loaded {table_name}: {len(fact_tables[table_name])} rows"
                )
            except Exception as e:
                logging.warning(f"Failed to load {table_name}: {e}")
                fact_tables[table_name] = pd.DataFrame()

        return fact_tables

    def get_all_data(self) -> Dict[str, pd.DataFrame]:
        """Get all dimension and fact tables"""
        all_data = {}

        # Get dimension tables
        dimension_tables = self.get_dimension_tables()
        all_data.update(dimension_tables)

        # Get fact tables
        fact_tables = self.get_fact_tables()
        all_data.update(fact_tables)

        return all_data

    def get_student_summary(self) -> pd.DataFrame:
        """Get comprehensive student summary with joined data"""
        query = """
        SELECT
            ds.student_id,
            ds.npm,
            ds.name,
            ds.email,
            ds.enrollment_date,
            ds.is_active,
            ds.program_name,
            ds.faculty_name,
            AVG(fa.cumulative_gpa) as avg_gpa,
            SUM(fa.total_credits) as total_credits,
            COUNT(DISTINCT fr.course_id) as courses_taken
        FROM dim_student ds
        LEFT JOIN fact_academic fa ON ds.student_id = fa.student_id
        LEFT JOIN fact_registration fr ON ds.student_id = fr.student_id
        GROUP BY ds.student_id, ds.npm, ds.name, ds.email,
                 ds.enrollment_date, ds.is_active, ds.program_name, ds.faculty_name
        ORDER BY ds.student_id
        """
        return self._execute_query(query)

    def get_course_summary(self) -> pd.DataFrame:
        """Get comprehensive course summary with enrollment data"""
        query = """
        SELECT
            dc.course_id,
            dc.course_code,
            dc.course_name,
            dc.credits,
            dc.program_name,
            dc.faculty_name,
            COUNT(DISTINCT fr.student_id) as total_enrollments,
            AVG(fg.final_grade) as avg_grade,
            COUNT(DISTINCT ft.lecturer_id) as lecturers_assigned
        FROM dim_course dc
        LEFT JOIN fact_registration fr ON dc.course_id = fr.course_id
        LEFT JOIN fact_grade fg ON dc.course_id = fg.course_id
        LEFT JOIN fact_teaching ft ON dc.course_id = ft.course_id
        GROUP BY dc.course_id, dc.course_code, dc.course_name,
                 dc.credits, dc.program_name, dc.faculty_name
        ORDER BY total_enrollments DESC
        """
        return self._execute_query(query)

    def get_lecturer_summary(self) -> pd.DataFrame:
        """Get comprehensive lecturer summary with teaching data"""
        query = """
        SELECT
            dl.lecturer_id,
            dl.nip,
            dl.name,
            dl.email,
            dl.faculty_name,
            COUNT(DISTINCT ft.course_id) as courses_taught,
            AVG(ft.total_students) as avg_students_per_class,
            SUM(ft.teaching_hours) as total_teaching_hours
        FROM dim_lecturer dl
        LEFT JOIN fact_teaching ft ON dl.lecturer_id = ft.lecturer_id
        GROUP BY dl.lecturer_id, dl.nip, dl.name, dl.email, dl.faculty_name
        ORDER BY courses_taught DESC
        """
        return self._execute_query(query)

    def get_financial_summary(self) -> pd.DataFrame:
        """Get financial summary by semester and faculty"""
        query = """
        SELECT
            ds.semester_code,
            ds.academic_year,
            dst.faculty_name,
            COUNT(DISTINCT ff.student_id) as students_paid,
            SUM(ff.fee_amount) as total_fees_collected,
            AVG(ff.fee_amount) as avg_fee_per_student
        FROM fact_fee ff
        JOIN dim_semester ds ON ff.semester_id = ds.semester_id
        JOIN dim_student dst ON ff.student_id = dst.student_id
        GROUP BY ds.semester_code, ds.academic_year, dst.faculty_name
        ORDER BY ds.academic_year, ds.semester_code, dst.faculty_name
        """
        return self._execute_query(query)

    def get_performance_summary(self) -> pd.DataFrame:
        """Get academic performance summary"""
        query = """
        SELECT
            ds.semester_code,
            ds.academic_year,
            dst.faculty_name,
            dst.program_name,
            COUNT(DISTINCT fa.student_id) as total_students,
            AVG(fa.semester_gpa) as avg_semester_gpa,
            AVG(fa.cumulative_gpa) as avg_cumulative_gpa,
            AVG(fa.credits_passed) as avg_credits_passed
        FROM fact_academic fa
        JOIN dim_semester ds ON fa.semester_id = ds.semester_id
        JOIN dim_student dst ON fa.student_id = dst.student_id
        GROUP BY ds.semester_code, ds.academic_year, dst.faculty_name, dst.program_name
        ORDER BY ds.academic_year, ds.semester_code, dst.faculty_name
        """
        return self._execute_query(query)

    def get_grade_distribution(self) -> pd.DataFrame:
        """Get grade distribution across courses and faculties"""
        query = """
        SELECT
            fg.letter_grade,
            dc.faculty_name,
            dc.course_name,
            COUNT(*) as grade_count,
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY dc.faculty_name) as percentage
        FROM fact_grade fg
        JOIN dim_course dc ON fg.course_id = dc.course_id
        WHERE fg.letter_grade IS NOT NULL
        GROUP BY fg.letter_grade, dc.faculty_name, dc.course_name
        ORDER BY dc.faculty_name, fg.letter_grade
        """
        return self._execute_query(query)

    def get_room_utilization_summary(self) -> pd.DataFrame:
        """Get room utilization summary"""
        query = """
        SELECT
            dr.room_id,
            dr.building,
            dr.capacity,
            COUNT(DISTINCT fru.usage_date) as days_used,
            AVG(fru.actual_occupancy) as avg_occupancy,
            AVG(fru.utilization_rate) as avg_utilization_rate,
            MAX(fru.utilization_rate) as max_utilization_rate
        FROM dim_room dr
        LEFT JOIN fact_room_usage fru ON dr.room_id = fru.room_id
        GROUP BY dr.room_id, dr.building, dr.capacity
        ORDER BY avg_utilization_rate DESC
        """
        return self._execute_query(query)

    def close_connection(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close_connection()
