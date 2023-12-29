import re
from datetime import datetime
from uuid import uuid4

from course import Course
from review import Review


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def get_review(course: Course, form: dict) -> Review:
    required_fields = [
        "email",
        "nickname",
        "year",
        "rating",
        "difficulty",
        "workload",
        "review",
    ]

    for field in required_fields:
        if field not in form:
            raise ValidationError(f"Missing field: {field}")

    email = form["email"].strip()
    if not email.endswith("@student.uva.nl"):
        raise ValidationError("Email must end with @student.uva.nl")

    nickname = form["nickname"].strip()
    if not nickname:
        raise ValidationError("Nickname cannot be empty")

    year = form["year"].strip()
    if re.match(r"\d{4}/\d{4}", year):
        year1, year2 = map(int, year.split("/"))
        if year1 + 1 != year2:
            raise ValidationError("Wrong academic year")
    else:
        raise ValidationError("Wrong academic year")

    rating = int(form["rating"])
    if rating < 0 or rating > 10:
        raise ValidationError("Rating must be between 0 and 10")

    difficulty = int(form["difficulty"])
    if difficulty < 0 or difficulty > 10:
        raise ValidationError("Difficulty must be between 0 and 10")

    workload = int(form["workload"])
    if workload < 0 or workload > 168:
        raise ValidationError("Workload must be between 0 and 168")

    review = form["review"].strip()

    return Review(
        uuid=str(uuid4()),
        course_short_name=course.short_name,
        email=email,
        nickname=nickname,
        date=datetime.now(),
        year=year,
        rating=rating,
        difficulty=difficulty,
        workload=workload,
        review=review,
        is_verified=False,
    )
