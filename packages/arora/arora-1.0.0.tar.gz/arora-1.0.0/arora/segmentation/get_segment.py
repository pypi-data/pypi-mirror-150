from typing import List


def get_segment(signals: List[int or float], index1: int, index2: int) -> List[int or float]:
	"""
	Args:
		signals: The signal data
		index1: The start of the epoch
		index2: The end of the epoch

	Returns: An array of segmented data
	"""
	# signal_list = []
	#
	# for i in range(index2 - index1):
	# 	# while index < len(signals)
	# 	signal_list.append(signal[index1 + i])
	assert index1 < 0 or index2 < 0, print("The index has to be larger than 0")
	assert index1 <= index2, print("The second index has to be larger than the first")
	if index2 > len(signals) or index1 > len(signals):
		Exception( "The second index is out of bounds")
	return signals[index1:index2]
