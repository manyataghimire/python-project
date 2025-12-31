import subprocess
import sys
import os

# Change to the project directory
os.chdir(r'c:\Users\Dell\student_project\student_mgmt')

# Run the populate script
result = subprocess.run([sys.executable, 'populate_students.py'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("ERRORS:", result.stderr)
print(f"Return code: {result.returncode}")
