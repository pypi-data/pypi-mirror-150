import pyedflib as edf
from typing import List


def get_signals(file, signalname: str or List[str] = 'all') -> List[int or float] or List[List[int or float]]:
	"""
	TODO: Document/Comment the code and make it more readable
	Args:
		file: The edf file that is to be imported
		signalname: The name of the signals that is wanted, can also be a list of signals that are wanted

	Returns: list of all the signals that were requested

	"""

	signal = []
	# Get the signals and the signal headers from the file
	signals, signal_headers, _ = edf.highlevel.read_edf(file)

	index = 0
	# Check if the requested signals is all and return just the recently gathered signals
	if signalname == 'all':
		return signals
		# for eeg_dict in signal_headers:
		# 	signal.append(signals[index])
		# index += 1

	# Check if signals name is either list or string
	if type(signalname) == list:

		# Check for duplicates in the list and remove them
		signalname = __check_duplicates_and_remove(signalname)

		for eeg_dict in signal_headers:

			# Check if the label is in the parameter signal names
			if eeg_dict['label'] in signalname:
				# Remove the instance from the list to make the code more efficient
				signalname.remove(eeg_dict['label'])
				signal.append(signals[index])

			# Check if the list is empty and return the gathered signals
			if len(signalname) <= 0:
				return signal
			index += 1

	elif type(signalname) == str:

		for eeg_dict in signal_headers:

			if eeg_dict['label'] == signalname:
				s = signals[index]
				signal.append(signals[index])
			index += 1

	return signal


def __check_duplicates_and_remove(signal):
	"""
	Checks for duplicates and removes them

	Args:
		signal: A list of all signals labels

	Returns: list with all duplicates removed

	"""
	elems = []

	# Loop through the list
	for elem in signal:

		# If the instance is not in the created list insert it into the list
		if elem not in elems:
			elems.append(elem)

	return elems

