from dataclasses import dataclass

from flask import Flask, abort, redirect, render_template, request

from course import SQLiteCourseRepository
from emailsender import EmailSender
from review import SQLiteReviewRepository, get_review, ValidationError

app = Flask(__name__)


@dataclass
class Implementations:
    email_sender: callable
    course_repository: callable
    review_repository: callable


implementations = Implementations(
    email_sender=EmailSender(app),
    course_repository=SQLiteCourseRepository(),
    review_repository=SQLiteReviewRepository(),
)


@app.route("/")
def index():
    courses = implementations.course_repository.get_all()
    return render_template("index.html", courses=courses)


@app.get("/<course_short_name>")
def course_get(course_short_name: str):
    course = implementations.course_repository.get_by_short_name(course_short_name)
    if course is None:
        abort(404)

    reviews = implementations.review_repository.get_by_course(course)
    return render_template("course.html", course=course, reviews=reviews)


@app.get("/<course_short_name>/add-review")
def add_review_get(course_short_name: str):
    course = implementations.course_repository.get_by_short_name(course_short_name)
    if course is None:
        abort(404)

    return render_template("review.html", course=course)


@app.post("/<course_short_name>/add-review")
def add_review_post(course_short_name: str):
    course = implementations.course_repository.get_by_short_name(course_short_name)
    if course is None:
        abort(404)

    try:
        review = get_review(course, request.form)
        implementations.review_repository.save(review)
        implementations.email_sender.send(
            recipient=review.email,
            subject=f"{course.short_name} review confirmation",
            body=f"Please confirm the review using the following code: {review.uuid}",
        )
    except ValidationError as e:
        return render_template("review.html", course=course, error=e.message)

    return redirect("/verify-email")


@app.get("/verify-email")
def verify_email_get():
    return render_template("verify-email.html")


@app.post("/verify-email")
def verify_email_post():
    review = implementations.review_repository.get_by_uuid(request.form["code"])
    if review is None:
        return render_template("verify-email.html", error="Unknown code")

    review.is_verified = True
    implementations.review_repository.update(review)
    return redirect(f"/{review.course_short_name}")


if __name__ == "__main__":
    app.run()
