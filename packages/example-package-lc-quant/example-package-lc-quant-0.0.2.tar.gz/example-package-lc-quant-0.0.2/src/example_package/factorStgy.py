import numpy as np
import pandas as pd

class factorStgy():

	# ----------------------------------------- Parameters  
	# ---- R = X @ F + residul
	# ---- R: return (T * 1)
	# ---- X: exposure (T * m)
	# ---- F: factors (m * 1)
	# ---- T: number of time period
	# ---- m: number of factors

	_X = None

	# ----------------------------------------- Functions
	def addExposure(self, expo):
		col = expo.reshape(-1, 1)
		self._X = np.c_(self._X, col) if self._X != None else col

	def olsEst(self, R, X):
		return np.linalg.inv(X.T @ X) @ X.T @ R

	def backTest(self, R, period):
		netValue = 1
		R = R.reshape(-1, 1)
		for i in range(1, R.shape[0], period):
			Fi = self.olsEst(R[:i, :], self._X[:i, :])
			forcast = self._X[i-1, :] @ Fipy
			netValue = netValue * (1+R[i]) if forcast > 0 else netValue * (1-R[i])
		return netValue

