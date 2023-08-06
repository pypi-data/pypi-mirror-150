from typing import List


def segment_fs(signals: List[float or int], fs: int) -> List[List[int or float]]:
	"""

	Args:
		signals:
		fs:

	Returns:

	"""
	# Maybe have this in a separate file for everyone to use
	return [signals[x:x + fs] for x in range(0, len(signals), fs)]
