# Delta Lakehouse Project

<!-- TODO with emot-->

## 🛠️ To Do

- [ ] Use Pydantic to validate data source models
- [ ] Create command line interface for fast environment setup testing (Python Fire or Makefile)
- [ ] Add dashboard for data visualization

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

### Required Software

- **Python 3.13+**
- **uv** (Python package and project manager)
- **Docker & Docker Compose** (for MinIO storage)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/nseptio/delta-lakehouse
cd delta-lakehouse

# Install dependencies using uv
uv sync
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# The default configuration should work for local development:
# MINIO_ENDPOINT=localhost:9000
# MINIO_ACCESS_KEY=minioadmin
# MINIO_SECRET_KEY=minioadmin
# PGPASSWORD=postgres
# PGHOST=localhost
# PGUSER=postgres
# PGDATABASE=siak
```

### 3. Start MinIO Storage

```bash
# Start MinIO using Docker Compose
docker-compose up -d

# Verify MinIO is running
docker-compose ps
```

MinIO will be available at:

- **Console**: http://localhost:9001 (admin interface)
- **API**: http://localhost:9000 (S3-compatible API)
- **Credentials**: minioadmin / minioadmin

### 4. Configure Data Generation

Edit the data generation configuration:

```bash
# Edit configs/faker.yaml to adjust data volume
vim configs/faker.yaml
```

Example configuration:

```yaml
faculty: 2 # Number of faculties
program: 3 # Number of academic programs
lecturer: 3 # Number of lecturers
student: 20 # Number of students
room: 5 # Number of rooms
course: 5 # Number of courses
semester: 4 # Number of semesters
class_schedule: 5 # Number of class schedules
registration: 5 # Number of registrations
```

### 5. Generate Synthetic Data

```bash
# Generate data in Parquet format (default)
uv run python -m src.scripts.generate_data

# Generate data in CSV format
uv run python -m src.scripts.generate_data --format csv

# Generate data in JSON format
uv run python -m src.scripts.generate_data --format json

# Specify custom output directory
uv run python -m src.scripts.generate_data --format json --output data/custom
```

### 6. Seed Fake Data into PostgreSQL

```bash
# Seed generated data into PostgreSQL database
uv run python -m src.scripts.seed_data
```

### 7. Run the Main Application

This application demonstrates ETL processes from PostgreSQL to Delta Lake on MinIO.

```bash
# Ensure MinIO and PostgreSQL are running
uv run python src/main.py
```

## 🔧 Configuration

### Data Generation Settings

Modify `configs/faker.yaml` to control the volume of generated data:

```yaml
faculty: 15 # Adjust based on your needs
program: 65
lecturer: 1000
student: 45000 # Large datasets for testing
room: 350
course: 2500
semester: 8
class_schedule: 5000
registration: 200000 # Realistic university scale
```

### Logging Configuration

Adjust logging settings in [`configs/log.dev.yaml`](configs/log.dev.yaml).

### Environment Variables

Configure `.env` file for your environment:

```bash
# MinIO Configuration
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# PostgreSQL Configuration
PGPASSWORD=postgres
PGHOST=localhost
PGUSER=postgres
PGDATABASE=siak
```

## 📊 Data Generation

The project generates realistic academic data including:

- **Faculties**: Academic departments
- **Programs**: Degree programs (Bachelor's, Master's, PhD)
- **Lecturers**: Faculty members with specializations
- **Students**: Enrolled students with realistic profiles
- **Courses**: Academic courses with prerequisites
- **Rooms**: Classroom and facility data
- **Semesters**: Academic periods
- **Class Schedules**: Course timetables
- **Registrations**: Student course enrollments
- **Grades**: Academic performance records
- **Semester Fees**: Financial records
- **Academic Records**: Comprehensive student transcripts
