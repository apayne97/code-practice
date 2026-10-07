from random import random
import numpy as np
import pandas as pd

# Generate Intervals
total_intervals = 100
minimum_start = 0
maximum_end = 100
range_size = maximum_end - minimum_start
minimum_supported = 10

intervals = []
for _ in range(total_intervals):
    start = random() * range_size + minimum_start
    end = random() * (maximum_end - start) + start
    intervals.append([start, end])

def get_supported_intervals(intervals, minimum_supported):

    # cast intervals as a numpy array
    intervals_array = np.array(intervals)

    # sort by start, end
    sorted_intervals = intervals_array[np.lexsort((intervals_array[:, 1], intervals_array[:, 0]))]

    # track # of intervals in range as you increment through the start + ends

    # keep track of when you increase up past the minimum_supported and when you decrease down past it

    # return those ranges

supported_intervals = get_supported_intervals(intervals, minimum_supported)

print(supported_intervals)
