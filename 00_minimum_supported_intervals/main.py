import random
import numpy as np

# Generate Intervals
total_intervals = 50
minimum_start = 0
maximum_end = 100
range_size = maximum_end - minimum_start
max_interval_range = 10
MINIMUM_SUPPORT = 3

intervals = []
for _ in range(total_intervals):
    start = round(random.random() * range_size + minimum_start, 1)
    end = min(maximum_end, round(random.random() * (max_interval_range) + start, 1))
    intervals.append([start, end])

def get_supported_intervals(intervals, minimum_supported):

    # sort all of the points, labeled by whether they are a start or end
    dtype = [('value', 'float'), ('type', 'U20')]
    interval_points = []
    for interval in intervals:
        interval_points.append((interval[0], 'start'))
        interval_points.append((interval[1], 'end'))

    point_array = np.array(interval_points, dtype=dtype)

    sorted_point_array = np.sort(point_array)

    # increment through them checking if the # of overlapping intervals should go up or down
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

    # find where the number of supporting intervals goes up or down past the minimum supported number
    supported_intervals = []
    current_interval_start = None
    for point, n_supporting_intervals in zip(sorted_point_array, n_supporting_intervals_list):
        if current_interval_start:
            if n_supporting_intervals < minimum_supported:
                supported_intervals.append((current_interval_start, point[0], n_supporting_intervals + 1))
                current_interval_start = None
        else:
            if n_supporting_intervals >= minimum_supported:
                current_interval_start = point[0]

    return supported_intervals


supported_intervals = get_supported_intervals(intervals, MINIMUM_SUPPORT)

print(f"{len(supported_intervals)} intervals found!")
for start, end, n in supported_intervals:
    print(f"Start: {start}\t\t End: {end}\t\t # Supporting Intervals: {n}")
