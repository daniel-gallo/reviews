from datetime import datetime
from typing import Optional

import sqliteutils
from course import Course
from review import Review


class SQLiteReviewRepository:
    def __get_review_from_row(self, row: tuple) -> Review:
        (
            uuid,
            email,
            nickname,
            course_short_name,
            date,
            year,
            rating,
            difficulty,
            workload,
            review,
            is_verified,
        ) = row
        date = datetime.fromisoformat(date)
        return Review(
            uuid,
            email,
            nickname,
            course_short_name,
            date,
            year,
            rating,
            difficulty,
            workload,
            review,
            is_verified,
        )

    def get_by_course(self, course: Course) -> [Review]:
        query = """
        select uuid, email, nickname, course_short_name, date, year, rating, difficulty, workload, review, is_verified
        from reviews
        where course_short_name = :course_short_name
        and is_verified = 1
        order by date desc
        """

        reviews = []
        for row in sqliteutils.get_all(query, course_short_name=course.short_name):
            reviews.append(self.__get_review_from_row(row))

        return reviews

    def get_by_uuid(self, uuid: str) -> Optional[Review]:
        query = """
        select uuid, email, nickname, course_short_name, date, year, rating, difficulty, workload, review, is_verified
        from reviews
        where uuid = :uuid
        """
        row = sqliteutils.get_one(query, uuid=uuid)
        return self.__get_review_from_row(row) if row else None

    def save(self, review: Review):
        query = """
        insert into reviews 
        (uuid, email, nickname, course_short_name, date, year, rating, difficulty, workload, review, is_verified) 
        values 
        (:uuid,:email,:nickname,:course_short_name,:date,:year,:rating,:difficulty,:workload,:review,:is_verified)
        """
        sqliteutils.execute(
            query,
            uuid=review.uuid,
            email=review.email,
            nickname=review.nickname,
            course_short_name=review.course_short_name,
            date=review.date,
            year=review.year,
            rating=review.rating,
            difficulty=review.difficulty,
            workload=review.workload,
            review=review.review,
            is_verified=review.is_verified,
        )

    def update(self, review: Review):
        query = """
        update reviews
        set email = :email,
            nickname = :nickname,
            course_short_name = :course_short_name,
            date = :date,
            year = :year,
            rating = :rating,
            difficulty = :difficulty,
            workload = :workload,
            review = :review,
            is_verified = :is_verified
        where uuid = :uuid
        """
        sqliteutils.execute(
            query,
            uuid=review.uuid,
            email=review.email,
            nickname=review.nickname,
            course_short_name=review.course_short_name,
            date=review.date,
            year=review.year,
            rating=review.rating,
            difficulty=review.difficulty,
            workload=review.workload,
            review=review.review,
            is_verified=review.is_verified,
        )
