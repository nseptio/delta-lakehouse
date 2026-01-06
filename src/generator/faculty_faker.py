import uuid
from datetime import datetime

from faker import Faker

# Accurate list of UI's faculties (as of 2023)
faculty_options = [
    ("FH", "Fakultas Hukum"),
    ("FK", "Fakultas Kedokteran"),
    ("FG", "Fakultas Kedokteran Gigi"),
    ("FKM", "Fakultas Kesehatan Masyarakat"),
    ("FF", "Fakultas Farmasi"),
    ("FIK", "Fakultas Ilmu Keperawatan"),
    ("FMIPA", "Fakultas Matematika dan Ilmu Pengetahuan Alam"),
    ("FT", "Fakultas Teknik"),
    ("FASILKOM", "Fakultas Ilmu Komputer"),
    ("FEB", "Fakultas Ekonomi dan Bisnis"),
    ("FIB", "Fakultas Ilmu Budaya"),
    ("FISIP", "Fakultas Ilmu Sosial dan Ilmu Politik"),
    ("FPsi", "Fakultas Psikologi"),
    ("FIA", "Fakultas Ilmu Administrasi"),
    ("FKUI", "Fakultas Kedokteran Hewan"),
    ("Vokasi", "Sekolah Vokasi"),
]


def generate_faculty(fake: Faker, n=1):
    """
    Generate n random faculty entries
    Returns list of dicts with keys: faculty_id, faculty_code, faculty_name, created_at, updated_at
    """
    result = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Use all predefined faculties first
    used_faculty_codes = set()
    for i in range(min(n, len(faculty_options))):
        faculty_code, faculty_name = faculty_options[i]
        used_faculty_codes.add(faculty_code)
        result.append(
            {
                "faculty_id": str(uuid.uuid4()),
                "id": i + 1,
                "faculty_code": faculty_code,
                "faculty_name": faculty_name,
                "created_at": current_time,
                "updated_at": current_time,
            }
        )

    # If more faculties needed, generate random ones
    for i in range(len(faculty_options), n):
        while True:
            new_code = fake.random_letter().upper() + fake.random_letter().upper()
            if new_code not in used_faculty_codes:
                used_faculty_codes.add(new_code)
                break

        result.append(
            {
                "faculty_id": str(uuid.uuid4()),
                "id": i + 1,
                "faculty_code": new_code,
                "faculty_name": f"Fakultas {fake.word().capitalize()}",
                "created_at": current_time,
                "updated_at": current_time,
            }
        )

    return result
