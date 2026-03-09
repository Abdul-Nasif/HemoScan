import pickle
import pandas as pd

from sklearn.model_selection import cross_val_score
model = pickle.load(open("anemia_model.pkl", "rb"))
data = pd.read_csv("anemia_scaled.csv")

model = pickle.load(open("anemia_model.pkl", "rb"))
data = pd.read_csv("anemia_scaled.csv")

X = data.drop("Result", axis=1)
y = data["Result"]

scores = cross_val_score(model, X, y, cv=5)

print("Cross Validation Scores:", scores)
print("Average Accuracy:", scores.mean())