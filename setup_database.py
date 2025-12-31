#!/usr/bin/env python
"""
Populate the student database with 100 engineering students and 600 results
This script must be run from the project directory
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_mgmt.settings')
sys.path.insert(0, r'c:\Users\Dell\student_project\student_mgmt')

django.setup()

from student.models import Student, Result
import random

def populate_database():
    """Populate the database with 100 students and 600 results"""
    
    # Student names
    names = [
        "Aarav Singh", "Aditya Kumar", "Akshay Patel", "Amit Sharma", "Ananya Verma",
        "Aniket Desai", "Anuj Gupta", "Arjun Nair", "Arnav Chopra", "Aryan Iyer",
        "Ashish Rao", "Ashutosh Mishra", "Atharva Joshi", "Avni Malhotra", "Ayush Saxena",
        "Bhaskar Pillai", "Bhavna Singh", "Chirag Reddy", "Chitra Bhat", "Disha Sharma",
        "Divya Nambiar", "Harshit Agarwal", "Harsh Kumar", "Hema Sinha", "Hemant Jain",
        "Himanshu Verma", "Hiral Patel", "Isha Kapoor", "Isha Sharma", "Ishaan Khanna",
        "Ishita Gupta", "Jagjit Singh", "Jaya Dutta", "Jayant Malhar", "Jayesh Patel",
        "Jyoti Sharma", "Kanchan Verma", "Karan Arora", "Karthik Murthy", "Kashish Bhandari",
        "Katrina Mendes", "Keshav Kumar", "Khyati Singh", "Kiara Reddy", "Kiran Sharma",
        "Kisha Malhotra", "Kunal Verma", "Lakshadweep Singh", "Leena Gupta", "Mahesh Nair",
        "Manish Sharma", "Manjita Roy", "Manush Kumar", "Manya Bhat", "Meenal Patel",
        "Meera Singh", "Mihir Verma", "Misha Malhotra", "Mohit Desai", "Mohan Rao",
        "Naveen Kumar", "Neeraj Singh", "Neeti Sharma", "Neha Verma", "Neha Joshi",
        "Nidhi Kapoor", "Nikhil Pandey", "Nila Sharma", "Niman Bhatnagar", "Nishi Malhotra",
        "Nitesh Kumar", "Nitisha Singh", "Nivedita Bhat", "Nizam Ali", "Noor Fatima",
        "Ovia Singh", "Parth Sharma", "Parvati Gupta", "Pawan Kumar", "Payal Verma",
        "Payel Sinha", "Piya Sharma", "Pooja Malhotra", "Poonam Singh", "Pradeep Nair",
        "Pragati Verma", "Prajwal Kumar", "Pranav Sharma", "Pranjal Singh", "Prashant Joshi",
        "Priya Kapoor", "Priyanka Verma", "Priyesh Gupta", "Priyush Sharma", "Pulkit Agarwal",
        "Puru Singh", "Radhika Sharma", "Raghav Kumar", "Ragini Verma", "Rahul Patel"
    ]
    
    # Engineering courses
    courses = [
        "B.Tech CSE",
        "B.Tech ECE",
        "B.Tech Mechanical",
        "B.Tech Civil",
        "B.Tech Electrical"
    ]
    
    # Engineering subjects
    subjects = [
        "Mathematics",
        "Physics",
        "Data Structures",
        "Digital Electronics",
        "Engineering Drawing",
        "Programming Languages"
    ]
    
    # Clear existing data
    if Student.objects.exists():
        print("🗑️  Clearing existing data...")
        Result.objects.all().delete()
        Student.objects.all().delete()
        print("✓ Database cleared")
    
    print("\n📚 Adding 100 students with 6 subjects each...\n")
    
    # Create students and results
    for i, name in enumerate(names, 1):
        email = f"student{i}@engineering.edu"
        age = random.randint(18, 25)
        course = random.choice(courses)
        
        student = Student.objects.create(
            name=name,
            email=email,
            age=age,
            course=course
        )
        
        # Add 6 results for each student
        for subject in subjects:
            marks = random.randint(35, 100)
            result = Result.objects.create(
                student=student,
                subject=subject,
                marks=marks
            )
        
        if i % 10 == 0:
            print(f"✓ Added {i} students...")
    
    # Display summary
    total_students = Student.objects.count()
    total_results = Result.objects.count()
    avg_marks = Result.objects.aggregate(__avg=django.db.models.Avg('marks'))['__avg']
    
    print(f"\n{'='*50}")
    print(f"✅ DATABASE POPULATION COMPLETE!")
    print(f"{'='*50}")
    print(f"📊 Total Students: {total_students}")
    print(f"📈 Total Results: {total_results}")
    print(f"📕 Engineering Courses: {Student.objects.values('course').distinct().count()}")
    print(f"⭐ Average Marks: {round(avg_marks, 2) if avg_marks else 0}")
    print(f"{'='*50}")
    print(f"\n🎉 The website is ready to use!")
    print(f"Visit http://127.0.0.1:8000/ to see the changes")

if __name__ == '__main__':
    try:
        populate_database()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
