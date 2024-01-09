from os import environ

from flask import Flask, abort, redirect, render_template, request

from course import SQLiteCourseRepository
from emailsender import EmailSender, FakeEmailSender
from review import SQLiteReviewRepository, get_review, ValidationError

app = Flask(__name__)


course_repository = SQLiteCourseRepository()
review_repository = SQLiteReviewRepository()
# Use the real email sender when the environment variables are set (production and development with Docker)
# and the fake one for testing
email_sender = EmailSender(app) if "MAIL_USERNAME" in environ else FakeEmailSender()


@app.route("/")
def index():
    courses = course_repository.get_all()
    return render_template("index.html", courses=courses)


@app.get("/<course_short_name>")
def course_get(course_short_name: str):
    course = course_repository.get_by_short_name(course_short_name)
    if course is None:
        abort(404)

    reviews = review_repository.get_by_course(course)
    return render_template("course.html", course=course, reviews=reviews)


@app.get("/<course_short_name>/add-review")
def add_review_get(course_short_name: str):
    course = course_repository.get_by_short_name(course_short_name)
    if course is None:
        abort(404)

    return render_template("review.html", course=course)


@app.post("/<course_short_name>/add-review")
def add_review_post(course_short_name: str):
    course = course_repository.get_by_short_name(course_short_name)
    if course is None:
        abort(404)

    try:
        review = get_review(course, request.form)
        review_repository.save(review)
        email_sender.send(
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
    review = review_repository.get_by_uuid(request.form["code"])
    if review is None:
        return render_template("verify-email.html", error="Unknown code")

    review.is_verified = True
    review_repository.update(review)
    return redirect(f"/{review.course_short_name}")


if __name__ == "__main__":
    app.run()
