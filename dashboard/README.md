# University Analytics Dashboard

A comprehensive Streamlit dashboard for visualizing university dataset with interactive charts, key performance indicators, and detailed analytics.

## Features

### 📊 Dashboard Sections

1. **Key Performance Indicators (KPIs)**

   - Total students, courses, lecturers
   - Average GPA and total registrations
   - Real-time metrics calculation

2. **Student Analytics**

   - Student distribution by faculty
   - Enrollment trends over time
   - Active vs inactive students

3. **Academic Performance**

   - GPA distribution analysis
   - Letter grade distribution
   - Performance trends by semester

4. **Course Analytics**

   - Most popular courses by enrollment
   - Course credits distribution
   - Faculty-wise course offerings

5. **Financial Analytics**

   - Fee collection trends
   - Revenue by faculty
   - Payment completion rates

6. **Faculty Performance**

   - Teaching workload analysis
   - Faculty-wise student distribution
   - Lecturer productivity metrics

7. **Resource Utilization**

   - Room utilization rates
   - Capacity vs occupancy analysis
   - Building efficiency metrics

8. **Detailed Data Tables**
   - Filterable student information
   - Course catalog with enrollment data
   - Lecturer profiles and assignments
   - Academic records with performance metrics

### 🎛️ Interactive Features

- **Dynamic Filtering**: Filter by academic year, faculty, and semester
- **Real-time Updates**: Data refreshes automatically with cache management
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Export Capabilities**: Download charts and data tables
- **Drill-down Analysis**: Click on charts to explore detailed data

### 📈 Visualizations

- **Pie Charts**: Faculty distribution, grade distribution
- **Line Charts**: Enrollment trends, fee collection over time
- **Bar Charts**: Popular courses, room utilization, faculty workload
- **Histograms**: GPA distribution, credits distribution
- **Scatter Plots**: Room capacity vs utilization
- **Grouped Charts**: Semester performance comparison

## Installation

### Prerequisites

- Python 3.13 or higher
- UV package manager
- Access to the university DuckDB database

### Setup

1. **Navigate to the dashboard directory**:

   ```bash
   cd dashboard/
   ```

2. **Dependencies are managed by UV**:
   The required Streamlit dependency is already included in the project's `pyproject.toml` under the `vis` dependency group.

3. **Verify database access**:
   Ensure the DuckDB file exists at `../data/duckdb/siak.duckdb`

## Running the Dashboard

### Local Development

```bash
uv run streamlit run main.py
```

The dashboard will be available at `http://localhost:8501`

### Using the Run Script

```bash
./run_dashboard.sh
```

### Production Deployment

```bash
uv run streamlit run main.py --server.port 8080 --server.address 0.0.0.0
```

### Command Line Options

```bash
# Custom port
uv run streamlit run main.py --server.port 8080

# Custom database path
uv run streamlit run main.py -- --db-path /path/to/database.duckdb

# Debug mode
uv run streamlit run main.py --logger.level debug
```

## Configuration

### Database Configuration

The dashboard automatically connects to the DuckDB database. To use a different database:

1. Edit `config.py`:

   ```python
   self.db_path = "path/to/your/database.duckdb"
   ```

2. Or set environment variable:
   ```bash
   export DASHBOARD_DB_PATH="/path/to/database.duckdb"
   ```

### Customization

#### Colors and Styling

Edit `config.py` to customize colors:

```python
self.primary_color = "#1f77b4"
self.secondary_color = "#ff7f0e"
self.color_palette = ["#color1", "#color2", ...]
```

#### Dashboard Layout

Modify `main.py` to adjust layout:

```python
st.set_page_config(
    page_title="Custom Title",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"
)
```

#### Cache Settings

Adjust data refresh frequency in `config.py`:

```python
self.cache_ttl = 3600  # seconds (1 hour)
```

## File Structure

```
dashboard/
├── main.py                 # Main Streamlit application
├── data_extractor.py       # Database connection and data extraction
├── visualizations.py       # Chart and graph creation
├── metrics.py             # KPI and metrics calculation
├── config.py              # Configuration settings
├── run_dashboard.sh       # Launch script
└── README.md              # This file
```

## Data Schema

The dashboard works with the following university data warehouse schema:

### Dimension Tables

- `dim_student`: Student information with faculty and program details
- `dim_course`: Course catalog with credits and faculty mapping
- `dim_lecturer`: Faculty and lecturer information
- `dim_semester`: Academic periods and year information
- `dim_class`: Class schedules and lecturer assignments
- `dim_room`: Room capacity and building information

### Fact Tables

- `fact_registration`: Student course registrations
- `fact_grade`: Student grades and academic performance
- `fact_fee`: Financial transactions and fee payments
- `fact_academic`: Academic records and GPA tracking
- `fact_teaching`: Teaching workload and assignments
- `fact_room_usage`: Room utilization and occupancy data

## API and Extensions

### Adding New Visualizations

1. Create new visualization method in `visualizations.py`:

   ```python
   def create_custom_chart(self) -> Optional[go.Figure]:
       # Your chart logic here
       return fig
   ```

2. Add to main dashboard in `main.py`:
   ```python
   custom_chart = visualizer.create_custom_chart()
   if custom_chart:
       st.plotly_chart(custom_chart, use_container_width=True)
   ```

### Adding New Metrics

1. Add calculation method in `metrics.py`:

   ```python
   def get_custom_metrics(self) -> Dict[str, float]:
       # Your metrics calculation here
       return metrics
   ```

2. Display in dashboard:
   ```python
   custom_metrics = metrics_calculator.get_custom_metrics()
   st.metric("Custom KPI", custom_metrics['value'])
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Error**:

   ```
   Error: No such file or directory: '../data/duckdb/siak.duckdb'
   ```

   - Verify the database file exists
   - Check file permissions
   - Update path in `config.py`

2. **Import Errors**:

   ```
   ModuleNotFoundError: No module named 'streamlit'
   ```

   - Run with UV: `uv run streamlit run main.py`
   - Ensure you're in the project root or dashboard directory

3. **Memory Issues with Large Datasets**:

   - Increase cache TTL in config
   - Implement data pagination
   - Add data filtering before visualization

4. **Performance Issues**:
   - Enable Streamlit caching: `@st.cache_data`
   - Optimize database queries
   - Reduce data refresh frequency

### Debug Mode

Run with debug logging:

```bash
uv run streamlit run main.py --logger.level debug
```

### Performance Monitoring

Add performance tracking:

```python
import time
start_time = time.time()
# Your operation
st.write(f"Operation took {time.time() - start_time:.2f} seconds")
```

## Contributing

### Development Workflow

1. Create feature branch
2. Add new functionality
3. Test with sample data
4. Update documentation
5. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Add type hints where appropriate
- Include docstrings for functions
- Add error handling for database operations

## License

This dashboard is part of the Delta Lakehouse project. See the main project license for details.

## Support

For issues and questions:

1. Check this README and troubleshooting section
2. Review the main project documentation
3. Check database connectivity and data availability
4. Open an issue in the project repository
