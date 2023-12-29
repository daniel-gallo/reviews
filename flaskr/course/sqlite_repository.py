from typing import Optional

import sqliteutils
from course import Course


class SQLiteCourseRepository:
    base_query = """
    select 
        name, 
        short_name, 
        block, 
        credits, 
        avg(case when is_verified = 1 then rating end) as mean_rating, 
        avg(case when is_verified = 1 then difficulty end) as mean_difficulty, 
        avg(case when is_verified = 1 then workload end) as mean_workload
    from courses
    left join reviews on courses.short_name = reviews.course_short_name
    """

    def get_all(self) -> [Course]:
        query = self.base_query + " group by short_name"
        courses = []

        for row in sqliteutils.get_all(query):
            courses.append(Course(*row))

        return courses

    def get_by_short_name(self, short_name: str) -> Optional[Course]:
        query = self.base_query + " where short_name = :short_name"

        row = sqliteutils.get_one(query, short_name=short_name)
        return Course(*row) if row else None
