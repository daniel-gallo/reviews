from dataclasses import dataclass


@dataclass
class Course:
    name: str
    short_name: str
    block: int
    credits: int
    mean_rating: float
    mean_difficulty: float
    mean_workload: float
