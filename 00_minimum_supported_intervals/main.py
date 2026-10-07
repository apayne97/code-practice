from random import random

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

print(intervals)
