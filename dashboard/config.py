"""
Configuration Module
Manages dashboard configuration and settings
"""

from pathlib import Path


class DashboardConfig:
    """Configuration settings for the university dashboard"""

    def __init__(self):
        # Base paths
        self.dashboard_dir = Path(__file__).parent
        self.project_root = self.dashboard_dir.parent

        # Database configuration
        self.db_path = self.project_root / "data" / "duckdb" / "siak.duckdb"

        # Dashboard settings
        self.app_title = "University Analytics Dashboard"
        self.app_icon = "🎓"
        self.layout = "wide"

        # Styling
        self.primary_color = "#1f77b4"
        self.secondary_color = "#ff7f0e"

        # Data refresh settings
        self.cache_ttl = 3600  # 1 hour in seconds

        # Pagination settings
        self.max_rows_per_table = 1000

        # Chart settings
        self.default_chart_height = 400
        self.color_palette = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ]

    def get_db_path(self) -> str:
        """Get the database path as string"""
        return str(self.db_path)

    def validate_paths(self) -> bool:
        """Validate that required paths exist"""
        if not self.db_path.exists():
            print(f"Warning: Database file not found at {self.db_path}")
            return False
        return True
