import pickle
import numpy as np

model = pickle.load(open("student_model.pkl", "rb"))

sample = np.array([[5, 7, 80, 2, 1, 5, 3, 7]])

prediction = model.predict(sample)

print("Prediction:", prediction)