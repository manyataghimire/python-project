import os
import django
from django.utils.text import slugify
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_mgmt.settings')
django.setup()

from student.models import Student, Result

# Nepali names list
nepali_names = [
    "अञ्जल शर्मा", "राज कुमार", "प्रिया सिंह", "सुमेश पाण्डे", "नीता गुप्ता",
    "विकास मलिक", "ईशिता यादव", "रोहित वर्मा", "पारुल चौधरी", "अमित कुमार",
    "सीमा पटेल", "दिनेश जोशी", "अनीशा शर्मा", "राज पाल सिंह", "प्रिया मिश्रा",
    "संजय कुमार", "मीरा वर्मा", "नवीन चौहान", "उर्वशी सक्सेना", "आदित्य मलिक",
    "ज्योति सिंह", "विजय कुमार", "अनु शर्मा", "रवि भाई", "सुजॉय चटर्जी",
    "नीता कुलकर्णी", "सत्येंद्र सिंह", "सरिता वर्मा", "राकेश पांडे", "महिमा शर्मा",
    "हर्षित कुमार", "समीर पटेल", "कृष्णा वर्मा", "सुधीर यादव", "जया सिंह",
    "देवांश कुमार", "संधिता शर्मा", "वैभव मलिक", "गायत्री पांडे", "अर्जुन सिंह",
    "दिव्या वर्मा", "मोहित कुमार", "स्वाति भाई", "रोहन चौधरी", "भारती शर्मा",
    "निशांत पटेल", "अनुष्का वर्मा", "रिचर्ड सिंह", "विशाल कुमार", "रिया शर्मा"
]

# Courses
courses = ["B.Tech", "BCA", "B.Sc", "B.Comm", "BBA"]

# Subjects
subjects = ["Mathematics", "English", "Science", "History", "Computer Science", "Economics"]

# Check if students already exist
if Student.objects.exists():
    print("Students already exist. Clearing database...")
    Result.objects.all().delete()
    Student.objects.all().delete()

print("Adding 50 students with results...")

for i, name in enumerate(nepali_names, 1):
    # Create student with unique email
    email = f"student{i}@university.edu"
    age = random.randint(18, 25)
    course = random.choice(courses)
    
    student = Student.objects.create(
        name=name,
        email=email,
        age=age,
        course=course
    )
    
    # Add 3-4 results for each student
    num_results = random.randint(3, 4)
    selected_subjects = random.sample(subjects, num_results)
    
    for subject in selected_subjects:
        marks = random.randint(35, 100)
        
        result = Result.objects.create(
            student=student,
            subject=subject,
            marks=marks
        )
        # Grade is auto-calculated in the model
        result.save()
    
    print(f"✓ Added {name} (ID: {student.id}) - {course} - {num_results} results")

print(f"\n✅ Successfully added 50 students with results!")
print(f"Total Students: {Student.objects.count()}")
print(f"Total Results: {Result.objects.count()}")
