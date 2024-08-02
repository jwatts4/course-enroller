from django.core.management.base import BaseCommand
from courses.models import Student, Preference, RankedCourse, Registration, Course


class Command(BaseCommand):
    help = "Clears the Student, Preference, RankedCourse, and Registration tables and resets occupied seats for all courses"

    def handle(self, *args, **kwargs):
        RankedCourse.objects.all().delete()
        Registration.objects.all().delete()
        Preference.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.update(
            occupied_seats=0
        )  # Reset occupied seats to zero for all courses
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully cleared specified tables and reset occupied seats"
            )
        )
