from dataclasses import dataclass


@dataclass
class Job:
    weight: int
    length: int


def sum_weighted_completion_times(jobs: list[Job]) -> int:
    weighted_sum = 0
    completion_time = 0
    for job in jobs:
        completion_time += job.length
        weighted_sum += job.weight * completion_time
    return weighted_sum


def greedy_difference(jobs: list[Job]) -> list[Job]:
    return sorted(jobs, key=lambda job: job.weight - job.length, reverse=True)


def greedy_ratio(jobs: list[Job]) -> list[Job]:
    return sorted(jobs, key=lambda job: job.weight/job.length, reverse=True)

