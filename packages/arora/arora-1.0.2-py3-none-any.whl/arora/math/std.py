import statistics
from typing import List


def std(signal_list: List[int or float]) -> float:
	"""
	Function that finds the given standard deviation of a given array

	:param signal_list:  a 1d array of edf signals
	:return: The standard deviation of the array
	"""
	if len(signal_list) < 2:
		raise Exception("Your array must contain at least two values")
	return statistics.stdev(signal_list)