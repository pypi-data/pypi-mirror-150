import signal
from typing import Tuple
import pandas as pd
import numpy as np
from arora.filter.EEG_freqbands import eeg_freq_bands


def welch_psd(signals: pd.DataFrame, sampling_frequency: int or float, filter_order: int) \
		-> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
	"""

	Args:
		signals: a segment of an edf signals in the form of a 1d array
		sampling_frequency: the frequency of the epoch in the form of an integer
		filter_order: the order of the filter

	Returns: Four arrays that contain the signals that have the relevant frequencies

	"""
	# Acknowledgement: Katrín Hera, M.Sc
	delta_band, theta_band, alpha_band, beta_band = eeg_freq_bands(signals, sampling_frequency, filter_order)

	window_size = int((sampling_frequency / 2) - 1)
	delta_nonbiased = delta_band - signal.savgol_filter(delta_band, window_size, filter_order)
	theta_nonbiased = theta_band - signal.savgol_filter(theta_band, window_size, filter_order)
	alpha_nonbiased = alpha_band - signal.savgol_filter(alpha_band, window_size, filter_order)
	beta_nonbiased = beta_band - signal.savgol_filter(beta_band, window_size, filter_order)
	F_AF3, delta_PSD = signal.welch(delta_nonbiased, sampling_frequency / 2, nperseg=len(delta_nonbiased))
	F_AF3, theta_PSD = signal.welch(theta_nonbiased, sampling_frequency / 2, nperseg=len(theta_nonbiased))
	F_AF3, alpha_PSD = signal.welch(alpha_nonbiased, sampling_frequency / 2, nperseg=len(alpha_nonbiased))
	F_AF3, beta_PSD = signal.welch(beta_nonbiased, sampling_frequency / 2, nperseg=len(beta_nonbiased))

	return delta_PSD, theta_PSD, alpha_PSD, beta_PSD
