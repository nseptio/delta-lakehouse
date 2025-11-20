"""
Metrics Module
Calculates key performance indicators and metrics for the university dashboard
"""

import logging
from typing import Dict

import pandas as pd


class UniversityMetrics:
    """Calculates various metrics and KPIs for university data"""

    def __init__(self, data: Dict[str, pd.DataFrame]):
        """
        Initialize with university data

        Args:
            data: Dictionary containing all dimension and fact tables
        """
        self.data = data

    def get_basic_metrics(self) -> Dict[str, int]:
        """Get basic count metrics"""
        metrics = {}

        try:
            metrics["total_students"] = len(
                self.data.get("dim_student", pd.DataFrame())
            )
            metrics["total_courses"] = len(self.data.get("dim_course", pd.DataFrame()))
            metrics["total_lecturers"] = len(
                self.data.get("dim_lecturer", pd.DataFrame())
            )
            metrics["total_faculties"] = (
                len(
                    self.data.get("dim_student", pd.DataFrame())[
                        "faculty_name"
                    ].unique()
                )
                if "dim_student" in self.data
                else 0
            )
            metrics["total_rooms"] = len(self.data.get("dim_room", pd.DataFrame()))

        except Exception as e:
            logging.error(f"Error calculating basic metrics: {e}")

        return metrics

    def get_academic_metrics(self) -> Dict[str, float]:
        """Get academic performance metrics"""
        metrics = {}

        try:
            if "fact_academic" in self.data and not self.data["fact_academic"].empty:
                academic_df = self.data["fact_academic"]

                metrics["avg_cumulative_gpa"] = academic_df["cumulative_gpa"].mean()
                metrics["avg_semester_gpa"] = academic_df["semester_gpa"].mean()
                metrics["avg_credits_passed"] = academic_df["credits_passed"].mean()
                metrics["avg_total_credits"] = academic_df["total_credits"].mean()

                # Calculate GPA distribution percentiles
                metrics["gpa_25th_percentile"] = academic_df["cumulative_gpa"].quantile(
                    0.25
                )
                metrics["gpa_50th_percentile"] = academic_df["cumulative_gpa"].quantile(
                    0.50
                )
                metrics["gpa_75th_percentile"] = academic_df["cumulative_gpa"].quantile(
                    0.75
                )

            if "fact_grade" in self.data and not self.data["fact_grade"].empty:
                grade_df = self.data["fact_grade"]

                metrics["avg_final_grade"] = grade_df["final_grade"].mean()

                # Calculate pass rate (assuming grades >= 60 are passing)
                passing_grades = grade_df[grade_df["final_grade"] >= 60]
                metrics["pass_rate"] = len(passing_grades) / len(grade_df) * 100

        except Exception as e:
            logging.error(f"Error calculating academic metrics: {e}")

        return metrics

    def get_financial_metrics(self) -> Dict[str, float]:
        """Get financial metrics"""
        metrics = {}

        try:
            if "fact_fee" in self.data and not self.data["fact_fee"].empty:
                fee_df = self.data["fact_fee"]

                metrics["total_fee_collected"] = fee_df["fee_amount"].sum()
                metrics["avg_fee_per_student"] = fee_df["fee_amount"].mean()
                metrics["median_fee"] = fee_df["fee_amount"].median()
                metrics["total_fee_transactions"] = len(fee_df)

                # Calculate payment completion rate
                if "dim_student" in self.data:
                    total_students = len(self.data["dim_student"])
                    students_paid = fee_df["student_id"].nunique()
                    metrics["payment_completion_rate"] = (
                        students_paid / total_students
                    ) * 100

        except Exception as e:
            logging.error(f"Error calculating financial metrics: {e}")

        return metrics

    def get_enrollment_metrics(self) -> Dict[str, float]:
        """Get enrollment and registration metrics"""
        metrics = {}

        try:
            if (
                "fact_registration" in self.data
                and not self.data["fact_registration"].empty
            ):
                registration_df = self.data["fact_registration"]

                metrics["total_registrations"] = len(registration_df)
                metrics["unique_students_registered"] = registration_df[
                    "student_id"
                ].nunique()
                metrics["unique_courses_registered"] = registration_df[
                    "course_id"
                ].nunique()
                metrics["avg_courses_per_student"] = (
                    metrics["total_registrations"]
                    / metrics["unique_students_registered"]
                )

                # Calculate course enrollment distribution
                course_enrollments = registration_df.groupby("course_id").size()
                metrics["avg_enrollment_per_course"] = course_enrollments.mean()
                metrics["max_enrollment_per_course"] = course_enrollments.max()
                metrics["min_enrollment_per_course"] = course_enrollments.min()

        except Exception as e:
            logging.error(f"Error calculating enrollment metrics: {e}")

        return metrics

    def get_faculty_metrics(self) -> Dict[str, Dict]:
        """Get metrics broken down by faculty"""
        faculty_metrics = {}

        try:
            if "dim_student" not in self.data or self.data["dim_student"].empty:
                return faculty_metrics

            faculties = self.data["dim_student"]["faculty_name"].unique()

            for faculty in faculties:
                faculty_metrics[faculty] = {}

                # Student count
                faculty_students = self.data["dim_student"][
                    self.data["dim_student"]["faculty_name"] == faculty
                ]
                faculty_metrics[faculty]["student_count"] = len(faculty_students)
                student_ids = faculty_students["student_id"].tolist()

                # Academic performance for this faculty
                if (
                    "fact_academic" in self.data
                    and not self.data["fact_academic"].empty
                ):
                    faculty_academic = self.data["fact_academic"][
                        self.data["fact_academic"]["student_id"].isin(student_ids)
                    ]

                    if not faculty_academic.empty:
                        faculty_metrics[faculty]["avg_gpa"] = faculty_academic[
                            "cumulative_gpa"
                        ].mean()
                        faculty_metrics[faculty]["avg_credits"] = faculty_academic[
                            "total_credits"
                        ].mean()

                # Fee collection for this faculty
                if "fact_fee" in self.data and not self.data["fact_fee"].empty:
                    faculty_fees = self.data["fact_fee"][
                        self.data["fact_fee"]["student_id"].isin(student_ids)
                    ]

                    if not faculty_fees.empty:
                        faculty_metrics[faculty]["total_fees"] = faculty_fees[
                            "fee_amount"
                        ].sum()
                        faculty_metrics[faculty]["avg_fee"] = faculty_fees[
                            "fee_amount"
                        ].mean()

                # Course count for this faculty
                if "dim_course" in self.data and not self.data["dim_course"].empty:
                    faculty_courses = self.data["dim_course"][
                        self.data["dim_course"]["faculty_name"] == faculty
                    ]
                    faculty_metrics[faculty]["course_count"] = len(faculty_courses)

                # Lecturer count for this faculty
                if "dim_lecturer" in self.data and not self.data["dim_lecturer"].empty:
                    faculty_lecturers = self.data["dim_lecturer"][
                        self.data["dim_lecturer"]["faculty_name"] == faculty
                    ]
                    faculty_metrics[faculty]["lecturer_count"] = len(faculty_lecturers)

        except Exception as e:
            logging.error(f"Error calculating faculty metrics: {e}")

        return faculty_metrics

    def get_teaching_metrics(self) -> Dict[str, float]:
        """Get teaching and workload metrics"""
        metrics = {}

        try:
            if "fact_teaching" in self.data and not self.data["fact_teaching"].empty:
                teaching_df = self.data["fact_teaching"]

                metrics["total_classes"] = len(teaching_df)
                metrics["avg_students_per_class"] = teaching_df["total_students"].mean()
                metrics["avg_teaching_hours"] = teaching_df["teaching_hours"].mean()
                metrics["total_teaching_hours"] = teaching_df["teaching_hours"].sum()

                # Calculate lecturer workload distribution
                lecturer_workload = teaching_df.groupby("lecturer_id").agg(
                    {"teaching_hours": "sum", "course_id": "nunique"}
                )

                metrics["avg_hours_per_lecturer"] = lecturer_workload[
                    "teaching_hours"
                ].mean()
                metrics["avg_courses_per_lecturer"] = lecturer_workload[
                    "course_id"
                ].mean()
                metrics["max_hours_per_lecturer"] = lecturer_workload[
                    "teaching_hours"
                ].max()
                metrics["min_hours_per_lecturer"] = lecturer_workload[
                    "teaching_hours"
                ].min()

        except Exception as e:
            logging.error(f"Error calculating teaching metrics: {e}")

        return metrics

    def get_room_utilization_metrics(self) -> Dict[str, float]:
        """Get room utilization metrics"""
        metrics = {}

        try:
            if (
                "fact_room_usage" in self.data
                and not self.data["fact_room_usage"].empty
            ):
                room_usage_df = self.data["fact_room_usage"]

                metrics["avg_utilization_rate"] = room_usage_df[
                    "utilization_rate"
                ].mean()
                metrics["max_utilization_rate"] = room_usage_df[
                    "utilization_rate"
                ].max()
                metrics["min_utilization_rate"] = room_usage_df[
                    "utilization_rate"
                ].min()
                metrics["avg_actual_occupancy"] = room_usage_df[
                    "actual_occupancy"
                ].mean()

                # Calculate room efficiency metrics
                if "dim_room" in self.data and not self.data["dim_room"].empty:
                    room_df = self.data["dim_room"]
                    room_usage_with_capacity = room_usage_df.merge(
                        room_df[["room_id", "capacity"]], on="room_id"
                    )

                    # Calculate actual utilization vs capacity
                    room_usage_with_capacity["capacity_utilization"] = (
                        room_usage_with_capacity["actual_occupancy"]
                        / room_usage_with_capacity["capacity"]
                        * 100
                    )

                    metrics["avg_capacity_utilization"] = room_usage_with_capacity[
                        "capacity_utilization"
                    ].mean()
                    metrics["total_room_capacity"] = room_df["capacity"].sum()
                    metrics["avg_room_capacity"] = room_df["capacity"].mean()

        except Exception as e:
            logging.error(f"Error calculating room utilization metrics: {e}")

        return metrics

    def get_semester_comparison(self) -> Dict[str, Dict]:
        """Get comparative metrics across semesters"""
        semester_metrics = {}

        try:
            if "dim_semester" not in self.data or self.data["dim_semester"].empty:
                return semester_metrics

            semesters = self.data["dim_semester"]["semester_code"].unique()

            for semester in semesters:
                semester_metrics[semester] = {}

                # Get semester ID
                semester_id = self.data["dim_semester"][
                    self.data["dim_semester"]["semester_code"] == semester
                ]["semester_id"].iloc[0]

                # Academic performance for this semester
                if (
                    "fact_academic" in self.data
                    and not self.data["fact_academic"].empty
                ):
                    semester_academic = self.data["fact_academic"][
                        self.data["fact_academic"]["semester_id"] == semester_id
                    ]

                    if not semester_academic.empty:
                        semester_metrics[semester]["avg_semester_gpa"] = (
                            semester_academic["semester_gpa"].mean()
                        )
                        semester_metrics[semester]["avg_cumulative_gpa"] = (
                            semester_academic["cumulative_gpa"].mean()
                        )
                        semester_metrics[semester]["total_credits"] = semester_academic[
                            "semester_credits"
                        ].sum()
                        semester_metrics[semester]["student_count"] = len(
                            semester_academic
                        )

                # Registrations for this semester
                if (
                    "fact_registration" in self.data
                    and not self.data["fact_registration"].empty
                ):
                    semester_registrations = self.data["fact_registration"][
                        self.data["fact_registration"]["semester_id"] == semester_id
                    ]
                    semester_metrics[semester]["total_registrations"] = len(
                        semester_registrations
                    )

                # Fee collection for this semester
                if "fact_fee" in self.data and not self.data["fact_fee"].empty:
                    semester_fees = self.data["fact_fee"][
                        self.data["fact_fee"]["semester_id"] == semester_id
                    ]

                    if not semester_fees.empty:
                        semester_metrics[semester]["total_fees"] = semester_fees[
                            "fee_amount"
                        ].sum()
                        semester_metrics[semester]["avg_fee"] = semester_fees[
                            "fee_amount"
                        ].mean()

        except Exception as e:
            logging.error(f"Error calculating semester comparison metrics: {e}")

        return semester_metrics

    def get_trend_analysis(self) -> Dict[str, Dict]:
        """Get trend analysis metrics"""
        trends = {
            "enrollment_trend": {},
            "performance_trend": {},
            "financial_trend": {},
        }

        try:
            # Enrollment trend analysis
            if "dim_student" in self.data and not self.data["dim_student"].empty:
                student_df = self.data["dim_student"].copy()
                student_df["enrollment_date"] = pd.to_datetime(
                    student_df["enrollment_date"]
                )
                student_df["enrollment_year"] = student_df["enrollment_date"].dt.year

                enrollment_by_year = student_df.groupby("enrollment_year").size()
                trends["enrollment_trend"]["by_year"] = enrollment_by_year.to_dict()

                if len(enrollment_by_year) > 1:
                    # Calculate growth rate
                    latest_year = enrollment_by_year.index[-1]
                    previous_year = enrollment_by_year.index[-2]
                    growth_rate = (
                        (
                            enrollment_by_year[latest_year]
                            - enrollment_by_year[previous_year]
                        )
                        / enrollment_by_year[previous_year]
                    ) * 100
                    trends["enrollment_trend"]["growth_rate"] = growth_rate

            # Performance trend analysis
            if (
                "fact_academic" in self.data
                and not self.data["fact_academic"].empty
                and "dim_semester" in self.data
                and not self.data["dim_semester"].empty
            ):
                academic_df = self.data["fact_academic"].merge(
                    self.data["dim_semester"][["semester_id", "academic_year"]],
                    on="semester_id",
                )

                performance_by_year = academic_df.groupby("academic_year").agg(
                    {
                        "cumulative_gpa": "mean",
                        "semester_gpa": "mean",
                        "credits_passed": "mean",
                    }
                )

                trends["performance_trend"]["gpa_by_year"] = performance_by_year[
                    "cumulative_gpa"
                ].to_dict()
                trends["performance_trend"]["semester_gpa_by_year"] = (
                    performance_by_year["semester_gpa"].to_dict()
                )

            # Financial trend analysis
            if (
                "fact_fee" in self.data
                and not self.data["fact_fee"].empty
                and "dim_semester" in self.data
                and not self.data["dim_semester"].empty
            ):
                fee_df = self.data["fact_fee"].merge(
                    self.data["dim_semester"][["semester_id", "academic_year"]],
                    on="semester_id",
                )

                financial_by_year = fee_df.groupby("academic_year").agg(
                    {"fee_amount": ["sum", "mean", "count"]}
                )

                trends["financial_trend"]["total_fees_by_year"] = financial_by_year[
                    ("fee_amount", "sum")
                ].to_dict()
                trends["financial_trend"]["avg_fees_by_year"] = financial_by_year[
                    ("fee_amount", "mean")
                ].to_dict()

        except Exception as e:
            logging.error(f"Error calculating trend analysis: {e}")

        return trends

    def get_all_metrics(self) -> Dict[str, Dict]:
        """Get all metrics in a single dictionary"""
        all_metrics = {
            "basic": self.get_basic_metrics(),
            "academic": self.get_academic_metrics(),
            "financial": self.get_financial_metrics(),
            "enrollment": self.get_enrollment_metrics(),
            "teaching": self.get_teaching_metrics(),
            "room_utilization": self.get_room_utilization_metrics(),
            "faculty_breakdown": self.get_faculty_metrics(),
            "semester_comparison": self.get_semester_comparison(),
            "trends": self.get_trend_analysis(),
        }

        return all_metrics
