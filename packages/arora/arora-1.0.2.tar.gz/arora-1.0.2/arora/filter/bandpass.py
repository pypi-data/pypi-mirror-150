import numpy as np
from scipy import signal
from typing import List

def bandpass(raw_signal: List[int or float], sampling_frequency: int or float,
             lower_cutoff: int or float, upper_cutoff: int or float,
             filter_order: int = 5) -> np.ndarray:
	"""
	Args:
		raw_signal: The EEG signals that is to be processed -> an array of float/integers value
		sampling_frequency: The frequency of the raw_signal -> a float or an integer
		lower_cutoff: The lower frequency value -> a float or an integer
		upper_cutoff: The upper frequency value -> a float or an integer
		filter_order: The maximum number of delay elements used in the filter circuit -> an integer value

	Returns: A filtered array

	"""
	w1 = lower_cutoff / (sampling_frequency / 2)
	w2 = upper_cutoff / (sampling_frequency / 2)
	b, a = signal.butter(filter_order, [w1, w2], btype = "bandpass", output = "ba")
	output_band = signal.lfilter(b, a, raw_signal)

	return output_band
