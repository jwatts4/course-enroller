from django import forms
from .models import Student, RankedCourse, Course


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_id", "first_name", "last_name"]


class RankedCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RankedCourseForm, self).__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.all().order_by("course_code")

    class Meta:
        model = RankedCourse
        fields = ["course"]  # the rank field is automatically set in the view
