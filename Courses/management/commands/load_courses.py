import random
from django.core.management.base import BaseCommand
from faker import Faker
from Courses.models import Course
from Accounts.models import CustomUser as User
from django.conf import settings


class Command(BaseCommand):
    help = "Generate fake courses and instructors"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create random instructors
        for _ in range(10):  
            email = fake.email()
            username = fake.user_name()
            instructor = User.objects.create_user(
                email=email,
                password="password123",  # Assigns a default password
                is_instructor=True,
                is_student=False,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Instructor {instructor.email} created")
            )

        # Create random courses for each instructor
        instructors = User.objects.filter(is_instructor=True)
        for instructor in instructors:
            for _ in range(5):  # Number of courses per instructor
                course = Course.objects.create(
                    title=fake.sentence(nb_words=6),  
                    description=fake.paragraph(
                        nb_sentences=3
                    ),
                    instructor=instructor,
                    price=round(
                        random.uniform(1000.00, 20000.00), 2
                    ),
                    category=fake.word(), 
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Course {course.title} created for instructor {instructor.email}"
                    )
                )
