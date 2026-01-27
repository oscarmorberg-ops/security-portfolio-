import numpy as np
from sklearn.ensemble import IsolationForest

data = np.array([[100], [120], [110], [5000], [115]])  # 5000=attack
model = IsolationForest(contamination=0.0)
model.fit(data)
print("Predictions:", model.predict(data))  # [1  1  1 -1  1]
