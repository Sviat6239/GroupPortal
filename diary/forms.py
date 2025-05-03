from django import forms
from diary.models import Student, Subject, Grade


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'})
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Subject Name'})
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('student', 'subject', 'grade')

        widgets = {
            'student': forms.Select(attrs={'placeholder': 'Select Student'}),
            'subject': forms.Select(attrs={'placeholder': 'Select Subject'}),
            'grade': forms.NumberInput(attrs={'placeholder': 'Enter Grade'})
        }
