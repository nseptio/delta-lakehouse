"""
Visualizations Module
Creates interactive charts and graphs for the university dashboard
"""

import logging
from typing import Dict, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class UniversityVisualizations:
    """Creates various visualizations for university data"""

    def __init__(self, data: Dict[str, pd.DataFrame]):
        """
        Initialize with university data

        Args:
            data: Dictionary containing all dimension and fact tables
        """
        self.data = data

        # Color palette for consistent styling
        self.colors = {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "info": "#17a2b8",
            "warning": "#ffc107",
            "danger": "#dc3545",
            "faculty_colors": px.colors.qualitative.Set3,
        }

    def create_faculty_distribution(self) -> Optional[go.Figure]:
        """Create pie chart showing student distribution by faculty"""
        try:
            if "dim_student" not in self.data or self.data["dim_student"].empty:
                return None

            faculty_counts = self.data["dim_student"]["faculty_name"].value_counts()

            fig = px.pie(
                values=faculty_counts.values,
                names=faculty_counts.index,
                title="Student Distribution by Faculty",
                color_discrete_sequence=self.colors["faculty_colors"],
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>Students: %{value}<br>Percentage: %{percent}<extra></extra>",
            )

            fig.update_layout(font=dict(size=12), showlegend=True, height=400)

            return fig

        except Exception as e:
            logging.error(f"Error creating faculty distribution chart: {e}")
            return None

    def create_enrollment_trend(self) -> Optional[go.Figure]:
        """Create line chart showing enrollment trends over time"""
        try:
            if "dim_student" not in self.data or self.data["dim_student"].empty:
                return None

            # Convert enrollment_date to datetime and extract year-month
            df = self.data["dim_student"].copy()
            df["enrollment_date"] = pd.to_datetime(df["enrollment_date"])
            df["enrollment_month"] = df["enrollment_date"].dt.to_period("M")

            enrollment_trend = (
                df.groupby("enrollment_month").size().reset_index(name="enrollments")
            )
            enrollment_trend["enrollment_month"] = enrollment_trend[
                "enrollment_month"
            ].astype(str)

            fig = px.line(
                enrollment_trend,
                x="enrollment_month",
                y="enrollments",
                title="Student Enrollment Trends Over Time",
                markers=True,
            )

            fig.update_traces(
                line=dict(color=self.colors["primary"], width=3), marker=dict(size=8)
            )

            fig.update_layout(
                xaxis_title="Enrollment Period",
                yaxis_title="Number of Students",
                height=400,
                xaxis=dict(tickangle=45),
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating enrollment trend chart: {e}")
            return None

    def create_gpa_distribution(self) -> Optional[go.Figure]:
        """Create histogram showing GPA distribution"""
        try:
            if "fact_academic" not in self.data or self.data["fact_academic"].empty:
                return None

            df = self.data["fact_academic"]
            if "cumulative_gpa" not in df.columns:
                return None

            fig = px.histogram(
                df,
                x="cumulative_gpa",
                title="Cumulative GPA Distribution",
                nbins=20,
                color_discrete_sequence=[self.colors["success"]],
            )

            fig.update_traces(
                hovertemplate="GPA Range: %{x}<br>Number of Students: %{y}<extra></extra>"
            )

            fig.update_layout(
                xaxis_title="Cumulative GPA",
                yaxis_title="Number of Students",
                height=400,
            )

            # Add vertical line for average GPA
            avg_gpa = df["cumulative_gpa"].mean()
            fig.add_vline(
                x=avg_gpa,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Avg GPA: {avg_gpa:.2f}",
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating GPA distribution chart: {e}")
            return None

    def create_grade_distribution(self) -> Optional[go.Figure]:
        """Create bar chart showing letter grade distribution"""
        try:
            if "fact_grade" not in self.data or self.data["fact_grade"].empty:
                return None

            df = self.data["fact_grade"]
            if "letter_grade" not in df.columns:
                return None

            grade_counts = df["letter_grade"].value_counts().sort_index()

            fig = px.bar(
                x=grade_counts.index,
                y=grade_counts.values,
                title="Letter Grade Distribution",
                color=grade_counts.values,
                color_continuous_scale="RdYlGn",
            )

            fig.update_traces(hovertemplate="Grade: %{x}<br>Count: %{y}<extra></extra>")

            fig.update_layout(
                xaxis_title="Letter Grade",
                yaxis_title="Number of Students",
                height=400,
                showlegend=False,
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating grade distribution chart: {e}")
            return None

    def create_popular_courses(self) -> Optional[go.Figure]:
        """Create bar chart showing most popular courses by enrollment"""
        try:
            if "fact_registration" not in self.data or "dim_course" not in self.data:
                return None

            # Join registration with course data
            registrations = self.data["fact_registration"]
            courses = self.data["dim_course"]

            if registrations.empty or courses.empty:
                return None

            course_popularity = (
                registrations.groupby("course_id")
                .size()
                .reset_index(name="enrollments")
            )
            course_popularity = course_popularity.merge(
                courses[["course_id", "course_name", "course_code"]], on="course_id"
            )

            # Get top 10 most popular courses
            top_courses = course_popularity.nlargest(10, "enrollments")

            fig = px.bar(
                top_courses,
                x="enrollments",
                y="course_name",
                orientation="h",
                title="Top 10 Most Popular Courses",
                color="enrollments",
                color_continuous_scale="Blues",
            )

            fig.update_traces(
                hovertemplate="<b>%{y}</b><br>Enrollments: %{x}<extra></extra>"
            )

            fig.update_layout(
                xaxis_title="Number of Enrollments",
                yaxis_title="Course",
                height=400,
                yaxis={"categoryorder": "total ascending"},
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating popular courses chart: {e}")
            return None

    def create_credits_distribution(self) -> Optional[go.Figure]:
        """Create bar chart showing course credits distribution"""
        try:
            if "dim_course" not in self.data or self.data["dim_course"].empty:
                return None

            df = self.data["dim_course"]
            if "credits" not in df.columns:
                return None

            credits_counts = df["credits"].value_counts().sort_index()

            fig = px.bar(
                x=credits_counts.index,
                y=credits_counts.values,
                title="Course Credits Distribution",
                color_discrete_sequence=[self.colors["info"]],
            )

            fig.update_traces(
                hovertemplate="Credits: %{x}<br>Number of Courses: %{y}<extra></extra>"
            )

            fig.update_layout(
                xaxis_title="Course Credits",
                yaxis_title="Number of Courses",
                height=400,
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating credits distribution chart: {e}")
            return None

    def create_fee_collection_trend(self) -> Optional[go.Figure]:
        """Create line chart showing fee collection trends"""
        try:
            if "fact_fee" not in self.data or "dim_semester" not in self.data:
                return None

            fees = self.data["fact_fee"]
            semesters = self.data["dim_semester"]

            if fees.empty or semesters.empty:
                return None

            # Join with semester data
            fee_trend = fees.merge(
                semesters[["semester_id", "semester_code", "academic_year"]],
                on="semester_id",
            )

            # Group by semester
            semester_fees = (
                fee_trend.groupby(["academic_year", "semester_code"])
                .agg({"fee_amount": "sum", "student_id": "count"})
                .reset_index()
            )

            semester_fees["period"] = (
                semester_fees["academic_year"] + " - " + semester_fees["semester_code"]
            )

            fig = px.line(
                semester_fees,
                x="period",
                y="fee_amount",
                title="Fee Collection Trends by Semester",
                markers=True,
            )

            fig.update_traces(
                line=dict(color=self.colors["warning"], width=3), marker=dict(size=8)
            )

            fig.update_layout(
                xaxis_title="Academic Period",
                yaxis_title="Total Fee Amount",
                height=400,
                xaxis=dict(tickangle=45),
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating fee collection trend chart: {e}")
            return None

    def create_fee_by_faculty(self) -> Optional[go.Figure]:
        """Create bar chart showing fee collection by faculty"""
        try:
            if "fact_fee" not in self.data or "dim_student" not in self.data:
                return None

            fees = self.data["fact_fee"]
            students = self.data["dim_student"]

            if fees.empty or students.empty:
                return None

            # Join with student data to get faculty info
            faculty_fees = fees.merge(
                students[["student_id", "faculty_name"]], on="student_id"
            )

            # Group by faculty
            fee_by_faculty = (
                faculty_fees.groupby("faculty_name")
                .agg({"fee_amount": "sum", "student_id": "count"})
                .reset_index()
            )

            fig = px.bar(
                fee_by_faculty,
                x="faculty_name",
                y="fee_amount",
                title="Total Fee Collection by Faculty",
                color="fee_amount",
                color_continuous_scale="Greens",
            )

            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Total Fees: %{y:,.0f}<extra></extra>"
            )

            fig.update_layout(
                xaxis_title="Faculty",
                yaxis_title="Total Fee Amount",
                height=400,
                xaxis=dict(tickangle=45),
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating fee by faculty chart: {e}")
            return None

    def create_faculty_workload(self) -> Optional[go.Figure]:
        """Create bar chart showing faculty teaching workload"""
        try:
            if "fact_teaching" not in self.data or "dim_lecturer" not in self.data:
                return None

            teaching = self.data["fact_teaching"]
            lecturers = self.data["dim_lecturer"]

            if teaching.empty or lecturers.empty:
                return None

            # Join with lecturer data
            faculty_workload = teaching.merge(
                lecturers[["lecturer_id", "faculty_name"]], on="lecturer_id"
            )

            # Group by faculty
            workload_summary = (
                faculty_workload.groupby("faculty_name")
                .agg({"teaching_hours": "sum", "lecturer_id": "nunique"})
                .reset_index()
            )

            workload_summary["avg_hours_per_lecturer"] = (
                workload_summary["teaching_hours"] / workload_summary["lecturer_id"]
            )

            fig = px.bar(
                workload_summary,
                x="faculty_name",
                y="avg_hours_per_lecturer",
                title="Average Teaching Hours per Lecturer by Faculty",
                color="avg_hours_per_lecturer",
                color_continuous_scale="Reds",
            )

            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Avg Hours: %{y:.1f}<extra></extra>"
            )

            fig.update_layout(
                xaxis_title="Faculty",
                yaxis_title="Average Teaching Hours",
                height=400,
                xaxis=dict(tickangle=45),
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating faculty workload chart: {e}")
            return None

    def create_room_utilization(self) -> Optional[go.Figure]:
        """Create scatter plot showing room utilization"""
        try:
            if "fact_room_usage" not in self.data or "dim_room" not in self.data:
                return None

            room_usage = self.data["fact_room_usage"]
            rooms = self.data["dim_room"]

            if room_usage.empty or rooms.empty:
                return None

            # Join with room data
            utilization = room_usage.merge(
                rooms[["room_id", "building", "capacity"]], on="room_id"
            )

            # Group by room
            room_util_summary = (
                utilization.groupby(["room_id", "building", "capacity"])
                .agg({"utilization_rate": "mean", "actual_occupancy": "mean"})
                .reset_index()
            )

            fig = px.scatter(
                room_util_summary,
                x="capacity",
                y="utilization_rate",
                size="actual_occupancy",
                color="building",
                title="Room Utilization vs Capacity",
                hover_data=["room_id"],
            )

            fig.update_traces(
                hovertemplate="<b>Room %{customdata[0]}</b><br>"
                + "Building: %{color}<br>"
                + "Capacity: %{x}<br>"
                + "Utilization Rate: %{y:.1f}%<br>"
                + "Avg Occupancy: %{marker.size:.1f}<extra></extra>"
            )

            fig.update_layout(
                xaxis_title="Room Capacity",
                yaxis_title="Utilization Rate (%)",
                height=400,
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating room utilization chart: {e}")
            return None

    def create_semester_performance_comparison(self) -> Optional[go.Figure]:
        """Create grouped bar chart comparing performance across semesters"""
        try:
            if "fact_academic" not in self.data or "dim_semester" not in self.data:
                return None

            academic = self.data["fact_academic"]
            semesters = self.data["dim_semester"]

            if academic.empty or semesters.empty:
                return None

            # Join with semester data
            performance = academic.merge(
                semesters[["semester_id", "semester_code"]], on="semester_id"
            )

            # Group by semester
            semester_performance = (
                performance.groupby("semester_code")
                .agg(
                    {
                        "semester_gpa": "mean",
                        "cumulative_gpa": "mean",
                        "credits_passed": "mean",
                    }
                )
                .reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    name="Semester GPA",
                    x=semester_performance["semester_code"],
                    y=semester_performance["semester_gpa"],
                    marker_color=self.colors["primary"],
                )
            )

            fig.add_trace(
                go.Bar(
                    name="Cumulative GPA",
                    x=semester_performance["semester_code"],
                    y=semester_performance["cumulative_gpa"],
                    marker_color=self.colors["secondary"],
                )
            )

            fig.update_layout(
                title="Academic Performance Comparison by Semester",
                xaxis_title="Semester",
                yaxis_title="GPA",
                barmode="group",
                height=400,
            )

            return fig

        except Exception as e:
            logging.error(f"Error creating semester performance comparison chart: {e}")
            return None
