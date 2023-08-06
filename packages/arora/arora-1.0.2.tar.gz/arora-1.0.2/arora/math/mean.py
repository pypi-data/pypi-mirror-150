from typing import List


def mean(signal_list: List[int or float]) -> float or int:
	"""
	Function that find the mean of a give array

	:param signal_list: a 1d array of edf signals
	:return: The mean of the array
	"""
	length = len(signal_list)
	if length == 0:
		return 0.0

	return float(sum(signal_list) / length)

