from typing import List
import pandas as pd
from scipy.io import loadmat


def load_mat(file: str) -> (List[int or float], pd.DataFrame):
	"""
	This function is a WIP
	Args:
		file:

	Returns:

	"""
	# If mat files all have the same format then hardcode how to insert the code into the dataframe and signals list
	data = loadmat(file)

	return "This function is still a WIP"
