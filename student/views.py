from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Avg
from .models import Student, Result
from .forms import StudentForm, ResultForm

def get_feedback(marks, grade):
    """Generate motivational feedback based on marks and grade"""
    if grade == 'A':
        if marks >= 95:
            return {
                'message': 'Outstanding Performance',
                'feedback': 'Excellent work! You are achieving exceptional results. Keep up this amazing performance and continue to push yourself higher!',
                'color': '#10b981'
            }
        else:
            return {
                'message': 'Excellent Work',
                'feedback': 'You are doing great! Your strong performance shows dedication and hard work. Keep maintaining this excellent standard!',
                'color': '#10b981'
            }
    elif grade == 'B':
        if marks >= 70:
            return {
                'message': 'Good Performance',
                'feedback': 'You are doing well! Your consistent performance is commendable. With a bit more effort, you can reach even higher marks!',
                'color': '#3b82f6'
            }
        else:
            return {
                'message': 'Good Effort',
                'feedback': 'You are on the right track! Continue working hard and focus on strengthening your weaker areas to improve further.',
                'color': '#3b82f6'
            }
    elif grade == 'C':
        return {
            'message': 'Keep Improving',
            'feedback': 'You have room for improvement. Don\'t get discouraged! Focus on your studies, seek help when needed, and work towards better results.',
            'color': '#f59e0b'
        }
    else:  # F grade
        return {
            'message': 'Time to Focus',
            'feedback': 'This is a challenging score, but remember - every failure is a step towards success! Identify your weak areas, seek extra help, and commit to improvement.',
            'color': '#ef4444'
        }

def calculate_gpa(results):
    """Calculate GPA from results - 4.0 scale"""
    if not results:
        return 0.0
    
    grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'F': 0.0}
    total_points = sum(grade_points.get(result.grade, 0) for result in results)
    gpa = total_points / len(results)
    return round(gpa, 2)

def home(request):
    """Dashboard with statistics"""
    total_students = Student.objects.count()
    total_courses = Student.objects.values('course').distinct().count()
    total_results = Result.objects.count()
    avg_marks = Result.objects.aggregate(Avg('marks'))['marks__avg']
    avg_marks = round(avg_marks, 2) if avg_marks else 0
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_results': total_results,
        'avg_marks': avg_marks,
    }
    return render(request, 'student/home_modern.html', context)

def student_list(request):
    """List all students with search functionality"""
    students = Student.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(course__icontains=search_query)
        )
    
    context = {
        'students': students,
        'search_query': search_query,
    }
    return render(request, 'student/student_list_modern.html', context)

def student_detail(request, id):
    """View individual student details with results"""
    student = get_object_or_404(Student, id=id)
    results = Result.objects.filter(student=student)
    
    # Add feedback for each result
    results_with_feedback = []
    for result in results:
        feedback = get_feedback(result.marks, result.grade)
        results_with_feedback.append({
            'result': result,
            'feedback': feedback
        })
    
    # Calculate average marks
    avg_marks = results.aggregate(Avg('marks'))['marks__avg']
    avg_marks = round(avg_marks, 2) if avg_marks else 0
    
    # Calculate GPA
    gpa = calculate_gpa(results)
    
    context = {
        'student': student,
        'results': results,
        'results_with_feedback': results_with_feedback,
        'avg_marks': avg_marks,
        'gpa': gpa,
    }
    return render(request, 'student/student_detail.html', context)

def add_student(request):
    """Add a new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'student/add_student_modern.html', {'form': form})

def edit_student(request, id):
    """Edit student information"""
    student = get_object_or_404(Student, id=id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', id=student.id)
    else:
        form = StudentForm(instance=student)

    return render(request, 'student/edit_student_modern.html', {'form': form, 'student': student})

def delete_student(request, id):
    """Delete a student"""
    student = get_object_or_404(Student, id=id)
    
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'student/confirm_delete.html', {'student': student})

# Results Management Views
def results_list(request):
    """List all results"""
    results = Result.objects.select_related('student').all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        results = results.filter(
            Q(student__name__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    context = {
        'results': results,
        'search_query': search_query,
    }
    return render(request, 'student/results_list_modern.html', context)

def add_result(request):
    """Add a new result"""
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result added successfully!')
            return redirect('results_list')
    else:
        form = ResultForm()
    
    return render(request, 'student/add_result_modern.html', {'form': form})

def edit_result(request, id):
    """Edit a result"""
    result = get_object_or_404(Result, id=id)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result updated successfully!')
            return redirect('results_list')
    else:
        form = ResultForm(instance=result)
    
    return render(request, 'student/edit_result_modern.html', {'form': form, 'result': result})

def delete_result(request, id):
    """Delete a result"""
    result = get_object_or_404(Result, id=id)
    
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Result deleted successfully!')
        return redirect('results_list')
    
    return render(request, 'student/confirm_delete_result.html', {'result': result})


