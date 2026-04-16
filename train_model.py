import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

np.random.seed(42)

n = 3000

study_hours = np.random.uniform(0, 10, n)
sleep_hours = np.random.uniform(4, 10, n)
social_media = np.random.uniform(0, 8, n)
stress = np.random.uniform(1, 10, n)
attendance = np.random.uniform(50, 100, n)

# realistic behavioral model
score = (
    study_hours * 8 +
    sleep_hours * 3 +
    attendance * 0.6 -
    social_media * 4 -
    stress * 2
)

score += np.random.normal(0, 4, n)
score = np.clip(score, 0, 100)

df = pd.DataFrame({
    "study_hours": study_hours,
    "sleep_hours": sleep_hours,
    "social_media": social_media,
    "stress": stress,
    "attendance": attendance,
    "score": score
})

X = df.drop("score", axis=1)
y = df["score"]

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))

print("Model trained and saved successfully!")
