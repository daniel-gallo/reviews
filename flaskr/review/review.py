from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    uuid: str
    email: str
    nickname: str
    course_short_name: str
    date: datetime
    year: str
    rating: int
    difficulty: int
    workload: int
    review: str
    is_verified: bool
