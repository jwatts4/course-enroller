from django.contrib import admin
from .models import Student, Course, Preference, RankedCourse, Registration

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Preference)
admin.site.register(RankedCourse)
admin.site.register(Registration)
