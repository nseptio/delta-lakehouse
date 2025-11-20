import random
import uuid
from datetime import datetime

from faker import Faker

# Accurate programs by faculty at UI (as of 2023)
program_options = {
    "FH": [
        ("H", "Ilmu Hukum"),
        ("HI", "Hukum Internasional"),
        ("HP", "Hukum Bisnis"),
        ("HAD", "Hukum Administrasi Negara"),
    ],
    "FK": [
        ("KD", "Pendidikan Dokter"),
        ("KK", "Ilmu Kedokteran Klinik"),
        ("KB", "Ilmu Biomedik"),
        ("KJ", "Ilmu Kesehatan Jiwa"),
        ("KA", "Ilmu Kesehatan Anak"),
        ("KBD", "Ilmu Bedah"),
    ],
    "FG": [
        ("GD", "Pendidikan Dokter Gigi"),
        ("GK", "Ilmu Kedokteran Gigi Klinik"),
        ("GO", "Ilmu Ortodonsia"),
    ],
    "FKM": [
        ("KM", "Ilmu Kesehatan Masyarakat"),
        ("KL", "Kesehatan Lingkungan"),
        ("KE", "Epidemiologi"),
        ("KG", "Gizi Kesehatan Masyarakat"),
    ],
    "FF": [
        ("FA", "Farmasi"),
        ("FK", "Farmasi Klinik"),
        ("FI", "Ilmu Kefarmasian"),
    ],
    "FIK": [
        ("IK", "Ilmu Keperawatan"),
        ("KJ", "Keperawatan Jiwa"),
        ("KA", "Keperawatan Anak"),
        ("KM", "Keperawatan Maternitas"),
    ],
    "FMIPA": [
        ("MA", "Matematika"),
        ("FI", "Fisika"),
        ("KM", "Kimia"),
        ("BI", "Biologi"),
        ("GF", "Geofisika"),
        ("ST", "Statistika"),
        ("GG", "Geografi"),
    ],
    "FT": [
        ("SI", "Teknik Sipil"),
        ("EL", "Teknik Elektro"),
        ("ME", "Teknik Mesin"),
        ("AR", "Arsitektur"),
        ("KI", "Teknik Kimia"),
        ("MT", "Teknik Metalurgi"),
        ("IN", "Teknik Industri"),
        ("LI", "Teknik Lingkungan"),
        ("PW", "Perencanaan Wilayah dan Kota"),
        ("KB", "Teknik Biomedik"),
        ("PI", "Teknik Perkapalan"),
    ],
    "FASILKOM": [
        ("IL", "Ilmu Komputer"),
        ("SI", "Sistem Informasi"),
        ("KJ", "Kecerdasan Buatan"),
        ("MT", "Teknologi Informasi"),
    ],
    "FEB": [
        ("EK", "Ilmu Ekonomi"),
        ("AK", "Akuntansi"),
        ("MN", "Manajemen"),
        ("IB", "Ilmu Ekonomi Islam"),
        ("BS", "Bisnis Digital"),
    ],
    "FIB": [
        ("SJ", "Sastra Jepang"),
        ("SI", "Sastra Inggris"),
        ("AR", "Arkeologi"),
        ("BL", "Bahasa dan Kebudayaan Korea"),
        ("BC", "Sastra Cina"),
        ("BD", "Sastra Daerah"),
        ("BI", "Sastra Indonesia"),
        ("SP", "Sastra Prancis"),
        ("SJ", "Sastra Jerman"),
        ("SA", "Sastra Arab"),
        ("SR", "Sastra Rusia"),
        ("BS", "Bahasa dan Kebudayaan Slavia"),
    ],
    "FISIP": [
        ("HI", "Hubungan Internasional"),
        ("SO", "Sosiologi"),
        ("KP", "Ilmu Politik"),
        ("KM", "Ilmu Komunikasi"),
        ("AN", "Antropologi Sosial"),
        ("KS", "Kesejahteraan Sosial"),
        ("KR", "Kriminologi"),
    ],
    "FPsi": [
        ("PS", "Psikologi"),
        ("PK", "Psikologi Klinis"),
        ("PO", "Psikologi Organisasi"),
        ("PP", "Psikologi Pendidikan"),
    ],
    "FIA": [
        ("AN", "Ilmu Administrasi Negara"),
        ("AB", "Ilmu Administrasi Bisnis"),
        ("AFP", "Ilmu Administrasi Fiskal"),
    ],
    "FKUI": [
        ("KH", "Kedokteran Hewan"),
        ("BT", "Bioteknologi Hewan"),
    ],
    "Vokasi": [
        ("AP", "Administrasi Perkantoran"),
        ("AK", "Akuntansi"),
        ("PR", "Hubungan Masyarakat"),
        ("PW", "Pariwisata"),
        ("BK", "Perbankan"),
        ("PO", "Perpajakan"),
        ("TI", "Teknologi Informasi"),
        ("AD", "Administrasi Asuransi & Aktuaria"),
        ("FK", "Fisioterapi"),
    ],
}


def generate_program(fake: Faker, faculties, n=10):
    """
    Generate n random program entries
    Returns list of dicts with keys: program_id, id, program_code, program_name, faculty_id, created_at, updated_at

    Args:
        faculties: List of faculty dicts from faculty_faker
        n: Number of programs to generate
    """
    result = []
    program_id = 1
    used_codes = set()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # First, add standard programs for each faculty
    for faculty in faculties:
        faculty_code = faculty["faculty_code"]
        faculty_id = faculty["id"]

        # Get program options for this faculty if available
        faculty_programs = program_options.get(faculty_code, [])

        # Add standard programs for this faculty
        for code_suffix, program_name in faculty_programs:
            program_code = f"{faculty_code}{code_suffix}"
            if program_code not in used_codes:
                used_codes.add(program_code)
                result.append(
                    {
                        "program_id": str(uuid.uuid4()),
                        "id": program_id,
                        "program_code": program_code,
                        "program_name": program_name,
                        "faculty_id": faculty_id,
                        "created_at": current_time,
                        "updated_at": current_time,
                    }
                )
                program_id += 1

                # Stop if we've reached the requested number
                if len(result) >= n:
                    return result

    # If we need more programs, generate random ones
    while len(result) < n:
        faculty = random.choice(faculties)
        faculty_id = faculty["id"]
        faculty_code = faculty["faculty_code"]

        # Generate random program code
        while True:
            code_suffix = fake.random_letter().upper() + fake.random_letter().upper()
            program_code = f"{faculty_code}{code_suffix}"
            if program_code not in used_codes:
                used_codes.add(program_code)
                break

        program_name = f"Program {fake.word().capitalize()} {fake.word().capitalize()}"

        result.append(
            {
                "program_id": str(uuid.uuid4()),
                "id": program_id,
                "program_code": program_code,
                "program_name": program_name,
                "faculty_id": faculty_id,
                "created_at": current_time,
                "updated_at": current_time,
            }
        )
        program_id += 1

    return result
