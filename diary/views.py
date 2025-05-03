from django.shortcuts import render, redirect, get_object_or_404
from diary.models import Student, Subject, Grade
from diary.forms import StudentForm, SubjectForm, GradeForm
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import user_passes_test
import json


# Create your views here.
# show the function for only admin
def is_admin(user):
    return user.is_superuser or user.is_staff


def diary_view(request):
    """
    Diary view function to render the diary page.
    """
    students = Student.objects.all()
    subjects = Subject.objects.all()
    grades = Grade.objects.all()

    grade_dict = {}
    for grade in grades:
        key = f"{grade.student.id}_{grade.subject.id}"
        if key not in grade_dict:
            grade_dict[key] = []
        grade_dict[key].append({
            'id': grade.id,
            'grade': grade.grade,
        })

    context = {
        'students': students,
        'subjects': subjects,
        'grade_dict_json': json.dumps(grade_dict, cls=DjangoJSONEncoder),
    }

    return render(request, 'diary/diary.html', context)


@user_passes_test(is_admin)
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary')
    else:
        form = StudentForm()
    return render(request, 'diary/add_student.html', {'form': form})


@user_passes_test(is_admin)
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('diary')
    else:
        form = StudentForm(instance=student)
    return render(request, 'diary/edit_student.html', {'form': form})


@user_passes_test(is_admin)
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary')
    else:
        form = SubjectForm()
    return render(request, 'diary/add_subject.html', {'form': form})


@user_passes_test(is_admin)
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('diary')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'diary/edit_subject.html', {'form': form})


@user_passes_test(is_admin)
def add_grade(request):
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary')
    else:
        form = GradeForm()
    return render(request, 'diary/grade.html', {'form': form})


@user_passes_test(is_admin)
def edit_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('diary')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'diary/grade.html', {'form': form})
