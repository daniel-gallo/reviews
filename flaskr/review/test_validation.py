import pytest

from course import Course
from review import ValidationError, get_review

course = Course(
    name="name",
    short_name="short_name",
    block=1,
    credits=6,
    mean_rating=10,
    mean_difficulty=10,
    mean_workload=10,
)

form = {
    "email": "user@student.uva.nl",
    "nickname": "nickname",
    "year": "2022/2023",
    "rating": 9,
    "difficulty": 7,
    "workload": 15,
    "review": "Very good course",
}


def test_email_verification():
    wrong_form = form.copy()
    wrong_form["email"] = "mail@gmail.com"

    with pytest.raises(ValidationError):
        get_review(course, wrong_form)
