import random
import numpy as np
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

# Generate Intervals
total_intervals = random.randint(10,20)
minimum_start = 0
maximum_end = 100
range_size = maximum_end - minimum_start
MINIMUM_SUPPORT = 3

intervals = []
for _ in range(total_intervals):
    start = round(random.random() * range_size + minimum_start, 1)
    end = round(random.random() * (maximum_end - start) + start, 1)
    intervals.append([start, end])

class Interval(BaseModel):
    start: float = Field(description="start of interval")
    end: float = Field(description="end of interval")
    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode='before')
    def validate_range(self):
        if self['end'] <= self['start']:
            raise ValueError("End of interval must be greater than start")
        return self

class SupportedInterval(Interval):
    number_of_supporting_intervals: int

    @field_validator('number_of_supporting_intervals', mode='before')
    @classmethod
    def validate_support(cls, n_supporting_intervals):
        if n_supporting_intervals < MINIMUM_SUPPORT:
            raise ValueError(f"Number of supporting intervals must be greater than {MINIMUM_SUPPORT}")




# def get_supported_intervals(intervals, minimum_supported):
#
#     # cast intervals as a numpy array
#     intervals_array = np.array(intervals)
#
#     # sort by start, end
#     sorted_intervals = intervals_array[np.lexsort((intervals_array[:, 1], intervals_array[:, 0]))]
#     print(sorted_intervals)

    # track # of intervals in range as you increment through the start + ends



    # supported_intervals = []
    # n_intervals_in_range = 0

    # for i, (start, end) in enumerate(sorted_intervals):
    #     if i == 0:
    #         current_interval = Interval(start=start, end=end)
    #     intervals_in_range = []
    #     # if start <= current_interval.start:
    #     #     n_intervals_in_range += 1
    #     # else:
    #     #     n_intervals_in_range += 1
    #     #     current_interval.start = start
    #
    #
    #     if start < current_interval.end:
    #         n_intervals_in_range += 1
    #         if n_intervals_in_range == minimum_supported:
    #             if start > current_interval.start:
    #                 current_interval.start = start
    #
    #     else:
    #         if n_intervals_in_range >= minimum_supported:
    #             supported_intervals.append(SupportedInterval(start=current_interval.start,
    #                                                          end=current_interval.end,
    #                                                          number_of_supporting_intervals=n_intervals_in_range))
    #         else:
    #             n_intervals_in_range -= 1
    #             current_interval = Interval(start=start, end=end)
    #     print(i, start, end)
    #     print(current_interval, n_intervals_in_range)
    # return supported_intervals

    # keep track of when you increase up past the minimum_supported and when you decrease down past it

def get_supported_intervals(intervals, minimum_supported):
    dtype = [('value', 'float'), ('type', 'U20')]
    interval_points = []
    for interval in intervals:
        interval_points.append((interval[0], 'start'))
        interval_points.append((interval[1], 'end'))

    point_array = np.array(interval_points, dtype=dtype)

    sorted_point_array = np.sort(point_array)

    n_supporting_intervals_list = []
    n_supported_intervals = 0
    for point in sorted_point_array:
        if point[1] == 'start':
            n_supported_intervals += 1
        else:
            n_supported_intervals -= 1

        if n_supported_intervals < 0:
            raise NotImplementedError(f"n_supported_intervals shouldn't be less than zero: {n_supported_intervals}")

        n_supporting_intervals_list.append(n_supported_intervals)

    supported_intervals = []
    current_interval_start = None
    for point, n_supporting_intervals in zip(sorted_point_array, n_supporting_intervals_list):
        if current_interval_start:
            if n_supporting_intervals < minimum_supported:
                supported_intervals.append((current_interval_start, point[0], n_supporting_intervals))
                current_interval_start = None
        else:
            if n_supporting_intervals >= minimum_supported:
                current_interval_start = point[0]

    return supported_intervals


supported_intervals = get_supported_intervals(intervals, MINIMUM_SUPPORT)

print(f"{len(supported_intervals)}")
