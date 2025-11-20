"""
University Data Analytics Dashboard
A comprehensive Streamlit dashboard for visualizing university dataset
"""

import streamlit as st

# Import custom modules
from data_extractor import DataExtractor
from metrics import UniversityMetrics
from visualizations import UniversityVisualizations

# Page configuration
st.set_page_config(
    page_title="University Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    """Load and cache data from DuckDB"""
    try:
        extractor = DataExtractor()
        return extractor.get_all_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def main():
    # Title and description
    st.markdown(
        '<h1 class="main-header">🎓 University Analytics Dashboard</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "### Comprehensive insights into university operations, student performance, and institutional metrics"
    )

    # Load data
    with st.spinner("Loading university data..."):
        data = load_data()

    if data is None:
        st.error("Failed to load data. Please check your database connection.")
        return

    # Initialize helper classes
    visualizer = UniversityVisualizations(data)
    metrics_calculator = UniversityMetrics(data)

    # Sidebar filters
    st.sidebar.header("📊 Dashboard Filters")

    # Academic Year filter
    academic_years = sorted(data["dim_semester"]["academic_year"].unique())
    selected_year = st.sidebar.selectbox("Select Academic Year", academic_years)

    # Faculty filter
    faculties = ["All"] + sorted(data["dim_student"]["faculty_name"].unique())
    selected_faculty = st.sidebar.selectbox("Select Faculty", faculties)

    # Semester filter
    semesters = sorted(data["dim_semester"]["semester_code"].unique())
    selected_semesters = st.sidebar.multiselect(
        "Select Semesters", semesters, default=semesters[:2]
    )

    # Filter data based on selection
    filtered_data = filter_data(
        data, selected_year, selected_faculty, selected_semesters
    )

    # Main dashboard content
    display_dashboard(
        filtered_data, visualizer, metrics_calculator, selected_year, selected_faculty
    )


def filter_data(data, academic_year, faculty, semesters):
    """Filter data based on user selections"""
    filtered_data = data.copy()

    # Filter by academic year
    semester_mask = filtered_data["dim_semester"]["academic_year"] == academic_year
    semester_ids = filtered_data["dim_semester"][semester_mask]["semester_id"].tolist()

    # Filter by faculty
    if faculty != "All":
        student_mask = filtered_data["dim_student"]["faculty_name"] == faculty
        student_ids = filtered_data["dim_student"][student_mask]["student_id"].tolist()
    else:
        student_ids = filtered_data["dim_student"]["student_id"].tolist()

    # Filter by selected semesters
    if semesters:
        semester_code_mask = filtered_data["dim_semester"]["semester_code"].isin(
            semesters
        )
        semester_ids = filtered_data["dim_semester"][semester_code_mask][
            "semester_id"
        ].tolist()

    # Apply filters to fact tables
    for table_name in ["fact_registration", "fact_grade", "fact_fee", "fact_academic"]:
        if table_name in filtered_data:
            if "semester_id" in filtered_data[table_name].columns:
                filtered_data[table_name] = filtered_data[table_name][
                    filtered_data[table_name]["semester_id"].isin(semester_ids)
                ]
            if "student_id" in filtered_data[table_name].columns:
                filtered_data[table_name] = filtered_data[table_name][
                    filtered_data[table_name]["student_id"].isin(student_ids)
                ]

    return filtered_data


def display_dashboard(
    data, visualizer, metrics_calculator, selected_year, selected_faculty
):
    """Display the main dashboard content"""

    # Key Metrics Section
    st.markdown(
        '<h2 class="section-header">📈 Key Performance Indicators</h2>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_students = len(data["dim_student"])
        st.metric("Total Students", f"{total_students:,}")

    with col2:
        total_courses = len(data["dim_course"])
        st.metric("Total Courses", f"{total_courses:,}")

    with col3:
        total_lecturers = len(data["dim_lecturer"])
        st.metric("Total Lecturers", f"{total_lecturers:,}")

    with col4:
        if "fact_academic" in data and not data["fact_academic"].empty:
            avg_gpa = data["fact_academic"]["cumulative_gpa"].mean()
            st.metric("Average GPA", f"{avg_gpa:.2f}")
        else:
            st.metric("Average GPA", "N/A")

    with col5:
        if "fact_registration" in data and not data["fact_registration"].empty:
            total_registrations = len(data["fact_registration"])
            st.metric("Total Registrations", f"{total_registrations:,}")
        else:
            st.metric("Total Registrations", "0")

    # Student Analytics Section
    st.markdown(
        '<h2 class="section-header">👥 Student Analytics</h2>', unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        # Student distribution by faculty
        faculty_dist = visualizer.create_faculty_distribution()
        if faculty_dist:
            st.plotly_chart(faculty_dist, use_container_width=True)

    with col2:
        # Student enrollment trends
        enrollment_trend = visualizer.create_enrollment_trend()
        if enrollment_trend:
            st.plotly_chart(enrollment_trend, use_container_width=True)

    # Academic Performance Section
    st.markdown(
        '<h2 class="section-header">🎯 Academic Performance</h2>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        # GPA distribution
        gpa_dist = visualizer.create_gpa_distribution()
        if gpa_dist:
            st.plotly_chart(gpa_dist, use_container_width=True)

    with col2:
        # Grade distribution
        grade_dist = visualizer.create_grade_distribution()
        if grade_dist:
            st.plotly_chart(grade_dist, use_container_width=True)

    # Course Analytics Section
    st.markdown(
        '<h2 class="section-header">📚 Course Analytics</h2>', unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        # Popular courses
        popular_courses = visualizer.create_popular_courses()
        if popular_courses:
            st.plotly_chart(popular_courses, use_container_width=True)

    with col2:
        # Course credits distribution
        credits_dist = visualizer.create_credits_distribution()
        if credits_dist:
            st.plotly_chart(credits_dist, use_container_width=True)

    # Financial Analytics Section
    st.markdown(
        '<h2 class="section-header">💰 Financial Analytics</h2>', unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        # Fee collection over time
        fee_trend = visualizer.create_fee_collection_trend()
        if fee_trend:
            st.plotly_chart(fee_trend, use_container_width=True)

    with col2:
        # Fee collection by faculty
        fee_by_faculty = visualizer.create_fee_by_faculty()
        if fee_by_faculty:
            st.plotly_chart(fee_by_faculty, use_container_width=True)

    # Faculty Performance Section
    st.markdown(
        '<h2 class="section-header">🏛️ Faculty Performance</h2>', unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        # Faculty workload
        faculty_workload = visualizer.create_faculty_workload()
        if faculty_workload:
            st.plotly_chart(faculty_workload, use_container_width=True)

    with col2:
        # Room utilization
        room_util = visualizer.create_room_utilization()
        if room_util:
            st.plotly_chart(room_util, use_container_width=True)

    # Detailed Tables Section
    st.markdown(
        '<h2 class="section-header">📊 Detailed Data Tables</h2>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Students", "Courses", "Lecturers", "Academic Records"]
    )

    with tab1:
        st.subheader("Student Information")
        if not data["dim_student"].empty:
            st.dataframe(data["dim_student"], use_container_width=True)
        else:
            st.info("No student data available for the selected filters.")

    with tab2:
        st.subheader("Course Information")
        if not data["dim_course"].empty:
            st.dataframe(data["dim_course"], use_container_width=True)
        else:
            st.info("No course data available for the selected filters.")

    with tab3:
        st.subheader("Lecturer Information")
        if not data["dim_lecturer"].empty:
            st.dataframe(data["dim_lecturer"], use_container_width=True)
        else:
            st.info("No lecturer data available for the selected filters.")

    with tab4:
        st.subheader("Academic Records")
        if "fact_academic" in data and not data["fact_academic"].empty:
            # Merge with student info for better readability
            academic_with_students = data["fact_academic"].merge(
                data["dim_student"][["student_id", "name", "npm"]], on="student_id"
            )
            st.dataframe(academic_with_students, use_container_width=True)
        else:
            st.info("No academic records available for the selected filters.")


if __name__ == "__main__":
    main()
