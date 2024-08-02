from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.db import transaction
from faker import Faker
from .models import Student, Preference, RankedCourse, Registration, Course
from .forms import StudentForm, RankedCourseForm
from .allocation_algorithm import AllocationAlgorithm

import logging

fake = Faker()
logger = logging.getLogger(__name__)  # had some debugging to do


def home(request):
    preference_count = Preference.objects.count()
    return render(request, "home.html", {"preference_count": preference_count})


def enter_preferences(request):
    # If the form has been submitted, process the data
    # i.e. POST request to the view
    if request.method == "POST":
        student_form = StudentForm(request.POST)
        RankedCourseFormSet = modelformset_factory(
            RankedCourse, form=RankedCourseForm, extra=10
        )
        formset = RankedCourseFormSet(request.POST)

        if student_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    student = student_form.save()
                    preference = Preference.objects.create(student=student)
                    logger.info(f"Created preference: {preference}")

                    for i, form in enumerate(formset):
                        if form.cleaned_data:
                            ranked_course = form.save(commit=False)
                            ranked_course.preference = preference
                            ranked_course.rank = (
                                i + 1
                            )  # infer the rank based on the order in the formset
                            ranked_course.save()
                            logger.info(f"Saved ranked course: {ranked_course}")

                return redirect("preferences_success")
            except Exception as e:
                logger.error(f"Error saving forms: {e}")
                return render(
                    request,
                    "courses/enter_preferences.html",
                    {
                        "student_form": student_form,
                        "formset": formset,
                        "error_message": "An error occurred while saving your preferences. Please try again.",
                    },
                )
        else:
            logger.info(f"Student form errors: {student_form.errors}")
            logger.info(f"Formset errors: {formset.errors}")
            return render(
                request,
                "courses/enter_preferences.html",
                {"student_form": student_form, "formset": formset},
            )

    # If the form has not been submitted, display the form
    # i.e. GET request to the view
    # Create a blank form and formset then pass them to the template
    else:
        student_form = StudentForm()
        RankedCourseFormSet = modelformset_factory(
            RankedCourse, form=RankedCourseForm, extra=10
        )
        formset = RankedCourseFormSet(queryset=RankedCourse.objects.none())

    return render(
        request,
        "courses/enter_preferences.html",
        {"student_form": student_form, "formset": formset},
    )


def preferences_success(request):
    return render(request, "courses/preferences_success.html")


def perform_allocation(request):
    if request.method == "POST":
        AllocationAlgorithm.allocate_courses()
        return redirect("allocation_results")

    preference_count = Preference.objects.count()
    return render(
        request,
        "courses/perform_allocation.html",
        {"preference_count": preference_count},
    )


def allocation_results(request):
    students = Student.objects.all()
    results = []

    for student in students:
        registrations = list(
            Registration.objects.filter(student=student).order_by("id")
        )
        course_names = [reg.course.course_name for reg in registrations]
        while len(course_names) < 5:
            course_names.append("")
        student_result = {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "registered_courses": course_names,
        }
        results.append(student_result)

    return render(request, "courses/allocation_results.html", {"results": results})


def course_list(request):
    courses = Course.objects.all().order_by("course_code")
    return render(request, "courses/course_list.html", {"courses": courses})


def clear_data(request):
    RankedCourse.objects.all().delete()
    Registration.objects.all().delete()
    Preference.objects.all().delete()
    Student.objects.all().delete()
    Course.objects.update(
        occupied_seats=0
    )  # Resets occupied seats to zero for all courses but doesn't touch other fields
    return redirect("clear_success")


def clear_success(request):
    return render(request, "courses/clear_success.html")


def sample_results(request):
    num_samples = 1000  # Number of sample entries to generate
    courses = list(Course.objects.all())

    with transaction.atomic():
        for _ in range(num_samples):
            student_id = str(fake.unique.random_number(digits=9))
            first_name = fake.first_name()
            last_name = fake.last_name()

            student = Student.objects.create(
                student_id=student_id, first_name=first_name, last_name=last_name
            )

            preference = Preference.objects.create(student=student)

            ranked_courses = fake.random_elements(
                elements=courses, length=5, unique=True
            )
            for i, course in enumerate(ranked_courses):
                RankedCourse.objects.create(
                    preference=preference, course=course, rank=i + 1
                )

    return redirect("sample_generation_success")


def sample_generation_success(request):
    preference_count = Preference.objects.count()
    return render(
        request,
        "courses/sample_generation_success.html",
        {"preference_count": preference_count},
    )


def about(request):
    return render(request, "about.html")
