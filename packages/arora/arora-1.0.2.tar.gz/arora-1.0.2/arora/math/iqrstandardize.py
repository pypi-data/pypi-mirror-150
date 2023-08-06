import numpy as np
from typing import List


def iqr_standardize(signals: List[int or float], lowerquantile: int, upperquantile: int):
	"""
	IQR standardization for the signals.
	Args:
		signals:
		lowerquantile:
		upperquantile:

	Returns:

	"""
	upperq, lowerq = np.percentile(signals, [upperquantile, lowerquantile])
	iqr = upperq - lowerq
	return (signals - np.median(signals)) / iqr