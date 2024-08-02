from django.core.management.base import BaseCommand
from courses.models import Course
import os
import random


class Command(BaseCommand):
    help = "Seed the database with courses from a text file"

    def handle(self, *args, **kwargs):
        course_file = "courses.txt"
        try:
            with open(course_file, "r") as file:
                for line in file:
                    course_code, course_name = line.strip().split(": ", 1)
                    Course.objects.get_or_create(
                        course_code=course_code,
                        defaults={
                            "course_name": course_name,
                            "total_seats": random.choice([25, 75, 125, 250]),
                            "occupied_seats": 0,
                        },
                    )
            self.stdout.write(
                self.style.SUCCESS("Successfully seeded the database with courses.")
            )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {course_file} not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
