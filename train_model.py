import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import joblib
import numpy as np 
class AnemiaModelTrain:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def train(self):


        from sklearn.model_selection import train_test_split, cross_val_score
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import accuracy_score, classification_report

        # Load dataset (RAW dataset, not scaled)
        data = pd.read_csv("anemia.csv")

        # Split features and target
        X = data.drop("Result", axis=1)
        y = data["Result"]

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Create scaler
        scaler = StandardScaler()

        # Fit scaler on training data
        X_train_scaled = scaler.fit_transform(X_train)

        # Transform test data
        X_test_scaled = scaler.transform(X_test)

        # Train model
        self.model.fit(X_train_scaled, y_train)

        # Test model
        predictions = self.model.predict(X_test_scaled)

        accuracy = accuracy_score(y_test, predictions)

        print("Model Accuracy:", accuracy)

        print("\nClassification Report:")
        print(classification_report(y_test, predictions))

        # Save model
        with open("anemia_model.pkl", "wb") as f:
            pickle.dump(self.model, f)

        # Save scaler
        with open("scaler.pkl", "wb") as f:
            pickle.dump(scaler, f)

        print("\nModel saved as anemia_model.pkl")
        print("Scaler saved as scaler.pkl")

        # Cross validation (on scaled full dataset)
        X_scaled = scaler.transform(X)

        scores = cross_val_score(self.model, X_scaled, y, cv=5)

        print("Cross Validation Scores:", scores)
        print("Average Accuracy:", scores.mean())
class AnemiaPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    def anemia_type(self, mcv):

        if mcv < 80:
            return "Microcytic Anemia"

        elif 80 <= mcv <= 100:
            return "Normocytic Anemia"

        else:
            return "Macrocytic Anemia"
    def risk_level(self, hb):

        if hb > 12:
            return "Normal"

        elif hb >= 10:
            return "Mild Risk"

        elif hb >= 7:
            return "Moderate Risk"

        else:
            return "Severe Risk"
        
    def recommendation(self, anemia_type):

        if anemia_type == "Microcytic Anemia":
            return "Possible Iron deficiency. Recommend iron-rich diet and supplements."

        elif anemia_type == "Normocytic Anemia":
            return "Further clinical evaluation recommended."

        elif anemia_type == "Macrocytic Anemia":
            return "Possible Vitamin B12 or Folate deficiency."

        else:
            return "No treatment required"
    def analyze_patient(self, gender, hb, mch, mchc, mcv):

        # anemia = self.model.predict([[hb, mcv]])
        model = joblib.load("anemia_model.pkl")
        scaler = joblib.load("scaler.pkl")

        # user input
        # gender = "Male"
        # hb = 10.5
        # mch = 22
        # mchc = 30
        # mcv = 75
        # convert gender
        gender = gender.lower()
        if gender == "male":
            gender = 1
        else:
            gender = 0

        # create input array
        user_input = pd.DataFrame(
        [[gender, hb, mch, mchc, mcv]],
        columns=["Gender","Hemoglobin","MCH","MCHC","MCV"]
        )
        # scale input
        scaled_input = scaler.transform(user_input)

        # predict
        prediction = model.predict(scaled_input)
        if prediction[0] == 0:
            return {
                "Diagnosis": "No Anemia",
                "Risk": "Low",
                "Recommendation": "Healthy",
                "Type":"None"
            }

        type_anemia = self.anemia_type(mcv)
        risk = self.risk_level(hb)
        advice = self.recommendation(type_anemia)

        return {
            "Diagnosis": "Anemia",
            "Type": type_anemia,
            "Risk": risk,
            "Recommendation": advice
        }
    def predict(self, gender, hb, mch, mchc, mcv):
        result = self.analyze_patient(gender, hb, mch, mchc, mcv)
        print("Patient Analysis:")
        for key, value in result.items():
            print(f"{key}: {value}")
        return result

    def scale_input(self, gender, hb, mch, mchc, mcv):
        scaler = joblib.load("scaler.pkl")
        gender = gender.lower()

        if gender == "male":
            gender = 1
        else:
            gender = 0

        # create input array
        user_input = pd.DataFrame(
        [[gender, hb, mch, mchc, mcv]],
        columns=["Gender","Hemoglobin","MCH","MCHC","MCV"]
        )
        # scale input
        scaled_input = scaler.transform(user_input) 
        return scaled_input
      
# model = AnemiaPredictor()
# model.predict("femail",15.9,25.4,28.3,72)
# train = AnemiaModelTrain()
# train.train()
        