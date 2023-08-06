from typing import List
import numpy as np
from scipy.fftpack import fft


def fourier(signals: List[List[int or float]], sampling_frequency: int or float) -> List[np.ndarray]:
	"""

	Args:
		signals: The segmented data in a list.
		sampling_frequency: The sampling frequency of the data.

	Returns:

	"""
	return_list = []
	T = 1 / sampling_frequency
	for i in signals:
		yf = fft(i)
		yf = np.array(yf)
		return_list.append(yf)
	return return_list
