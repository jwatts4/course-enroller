import random
from .models import Student, Course, Preference, Registration


class AllocationAlgorithm:
    @staticmethod
    def allocate_courses():
        # Get all of the preferences and shuffle them
        preferences = Preference.objects.all()
        shuffled_preferences = list(preferences)
        random.shuffle(shuffled_preferences)

        # Get all of the courses and create a dictionary with course_code as the key
        courses = Course.objects.all()
        course_dict = {course.course_code: course for course in courses}

        # Loop, from the first preference to the last, and allocate courses
        # This will try to allocate the top 5 preferences of each student
        # all at once, before moving on to the next student.
        for preference in shuffled_preferences:
            allocated_courses = 0
            ranked_courses = preference.get_top_preferences(10)
            for ranked_course in ranked_courses:
                course = ranked_course.course
                if allocated_courses < 5 and course.seats_available() > 0:
                    course.decrease_seat_count()
                    Registration.objects.create(
                        student=preference.student, course=course
                    )
                    allocated_courses += 1
