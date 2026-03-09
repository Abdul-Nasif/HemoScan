import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# Load dataset
class scale_data:
    def __init__(self):
        self.data = pd.read_csv("anemia.csv")
    def scale(self):
    # Separate features and target
        X = self.data.drop("Result", axis=1)
        y = self.data["Result"]

        # Columns to scale
        scale_columns = ["Hemoglobin", "MCH", "MCHC", "MCV"]

        # Create scaler
        scaler = StandardScaler()

        # Scale selected columns
        X[scale_columns] = scaler.fit_transform(X[scale_columns])

        # Combine scaled features and target
        scaled_data = pd.concat([X, y], axis=1)

        # Save scaled dataset
        scaled_data.to_csv("anemia_scaled.csv", index=False)

        # Save scaler for future predictions
        with open("scaler.pkl", "wb") as f:
            pickle.dump(scaler, f)

        print("✅ Scaled dataset saved as anemia_scaled.csv")
        print("✅ Scaler saved as scaler.pkl")

        print("\nPreview of scaled data:")
        print(scaled_data.head())

scale = scale_data()
scale.scale()