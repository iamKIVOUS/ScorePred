import subprocess
import datetime
import os
import sys

# Setup Django environment so we can call its management commands
def setup_django():
    backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
    sys.path.append(backend_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Logging utility
def log(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

# Run a Python script
def run_script(script_name):
    log(f"Running {script_name}...")
    subprocess.run(["python", f"scrape/{script_name}"])
    log(f"{script_name} completed.\n")

# Run Django import_csv command
def run_import_command():
    log("Importing CSVs into Django DB...")
    subprocess.run(["python", "backend/manage.py", "import_csv"])
    log("CSV import completed.\n")

def main():
    log("=== Starting IPL Scraper Automation ===")
    run_script("urlScrap.py")
    run_script("batterScrap.py")
    run_script("bowlerScrap.py")
    run_script("matchScrap.py")
    run_import_command()
    log("=== All Tasks Completed ===")

if __name__ == "__main__":
    setup_django()
    main()
