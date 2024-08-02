from django.db import models


class Student(models.Model):
    """
    Models a student with a unique student ID, first name, last name, and email

    A student has a one-to-one relationship with Preference and a many-to-many
    relationship with Course through Registration
    """

    student_id = models.CharField(max_length=9, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)

    def generate_email(self):
        """Match Laurier's student email format"""
        last_name = self.last_name.lower()
        if len(last_name) < 4:
            last_name_part = last_name + "x" * (4 - len(last_name))
        else:
            last_name_part = last_name[:4]
        student_id_part = str(self.student_id)[
            -4:
        ]  # Ensure student_id is treated as a string
        return f"{last_name_part}{student_id_part}@mylaurier.ca"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.email = self.generate_email()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Course(models.Model):
    """
    Models a course with a unique course code, name, and seat count

    A course has a one-to-many relationship with Preference and a many-to-many
    relationship with Student through Registration
    """

    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    total_seats = models.IntegerField(default=0)
    occupied_seats = models.IntegerField(default=0)

    def decrease_seat_count(self):
        if self.occupied_seats < self.total_seats:
            self.occupied_seats += 1
            self.save()

    def seats_available(self):
        return self.total_seats - self.occupied_seats

    def get_course_info(self):
        return f"{self.course_code}: {self.course_name}"

    def __str__(self):
        return self.get_course_info()


class Preference(models.Model):
    """
    A student's course preferences

    Part of a one-to-one relationship between Student and Preference.
    A student has a list of ranked courses as preferences, which
    are stored as a one-to-many relationship between Preference and RankedCourse
    """

    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    ranked_courses = models.ManyToManyField(
        "Course", through="RankedCourse", related_name="preferences"
    )

    def get_top_preferences(self, n):
        return self.rankedcourse_set.all().order_by("rank")[:n]

    def __str__(self):
        return f"Preferences of {self.student.get_full_name()}"


class RankedCourse(models.Model):
    """
    A student's ranked course preference

    Intermediate model to store the rank of a course in a student's preference list
    and establish a many-to-many relationship between Preference and Course
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rank = models.IntegerField()

    class Meta:
        unique_together = ("preference", "course")

    def __str__(self):
        return f"{self.preference.student.get_full_name()} - {self.course.get_course_info()} (Rank: {self.rank})"


class Registration(models.Model):
    """
    A student's registration for a course

    Intermediate model to enforce unique registration for each student-course
    and establish a many-to-many relationship between Student and Course
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student.get_full_name()} registered for {self.course.get_course_info()}"
