import matplotlib.pyplot as plt
import numpy as np
import os 
import joblib
import pandas as pd
from pdf_genarator import generate_medical_report


os.makedirs("reports", exist_ok=True)

class Visualizer:

    # Visualizer class for anemia data visualization
    # This class provides methods to create various charts for visualizing CBC parameters and hemoglobin levels.
    def __init__(self,gender,hb,mch,mchc,mcv):
        self.gender = gender
        self.hb = hb
        self.mch = mch
        self.mchc = mchc
        self.mcv = mcv
        self.model = joblib.load("anemia_model.pkl")
        self.scaler = joblib.load("scaler.pkl")


    def cbc_comparison_chart(self):
        
        parameters = ["Hemoglobin", "MCH", "MCHC", "MCV"]
        patient_values = [self.hb, self.mch, self.mchc, self.mcv]

        normal_min = [12, 27, 32, 80]
        normal_max = [16, 33, 36, 100]

        plt.figure(figsize=(8,5))

        plt.bar(parameters, patient_values,label = "Patient", color='skyblue')

        plt.plot(parameters, normal_min, marker='o', label="Min Normal", color='green')
        plt.plot(parameters, normal_max, marker='o', label="Max Normal", color='red')

        plt.title("CBC Parameter Comparison")
        plt.ylabel("Value")
        plt.legend()

    #    plt.show()
        plt.savefig("reports/cbc_comparison_chart.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("CBC comparison chart saved to reports/cbc_comparison_chart.png")



    def hemoglobin_risk_indicator(self):

        categories = ["Severe", "Moderate", "Mild", "Normal"]
        values = [7, 10, 12, 16]

        plt.figure(figsize=(8,2))

        plt.hlines(1, 0, 16, linewidth=10)

        plt.plot(self.hb, 1, marker="o", markersize=15)

        plt.text(self.hb, 1.05, f"Hb={self.hb}", ha='center')

        plt.title("Hemoglobin Risk Indicator")
        plt.yticks([])
        plt.xlim(0,16)

   #     plt.show()
        plt.savefig("reports/hemoglobin_risk_indicator.png",dpi = 300, bbox_inches='tight')
        plt.close()
        print("Hemoglobin risk indicator saved to reports/hemoglobin_risk_indicator.png")



    def radar_chart(self):

        labels = ["Hemoglobin", "MCH", "MCHC", "MCV"]
        patient_values = [self.hb, self.mch, self.mchc, self.mcv]

        normal_values = [14, 30, 34, 90]

        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

        patient_values += patient_values[:1]
        normal_values += normal_values[:1]
        angles = np.concatenate((angles, [angles[0]]))

        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111, polar=True)

        ax.plot(angles, patient_values, marker='o', label="Patient")
        ax.plot(angles, normal_values, marker='o', label="Normal")

        ax.fill(angles, patient_values, alpha=0.1)

        ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)

        plt.title("CBC Radar Analysis")
        plt.legend()

    #    plt.show()
        plt.savefig("reports/cbc_radar_chart.png", dpi=300, bbox_inches='tight')
        plt.close()
        print("CBC radar chart saved to reports/cbc_radar_chart.png")


        # Show Prediction Probability
    def plot_prediction_probability(self):
        prob = self.model.predict_proba(self.scale_input())[0]

        labels = ["No Anemia", "Anemia"]

        plt.figure(figsize=(6,4))
        plt.bar(labels, prob)

        plt.ylabel("Probability")
        plt.title("Model Prediction Confidence")

        plt.savefig("reports/prediction_probability.png", dpi=300)
        plt.close()
        print("Prediction probability chart saved to reports/prediction_probability.png")



# scaling the input for prediction
    def scale_input(self):
        scaler = joblib.load("scaler.pkl")
        self.gender = self.gender.lower()

        if self.gender == "male":
            self.gender = 1
        else:
            self.gender = 0

        # create input array
        user_input = pd.DataFrame(
        [[self.gender,self.hb, self.mch, self.mchc, self.mcv]],
        columns=["Gender","Hemoglobin","MCH","MCHC","MCV"]
        )
        # scale input
        scaled_input = scaler.transform(user_input) 
        return scaled_input
    
    # Feature Importance Graph
    def plot_feature_importance(self):

        features = ["Gender", "Hemoglobin", "MCH", "MCHC", "MCV"]

        importance = self.model.feature_importances_

        plt.figure(figsize=(6,4))

        plt.barh(features, importance)

        plt.xlabel("Importance")
        plt.title("Feature Importance in Anemia Prediction")

        plt.savefig("reports/feature_importance.png", dpi=300)
        plt.close()
        print("Feature importance chart saved to reports/feature_importance.png")


    # complete pipline 
    def pipline_visual(self):
        print("initiating pipline....")
        self.cbc_comparison_chart()
        self.hemoglobin_risk_indicator()
        self.radar_chart()
        self.plot_prediction_probability()
        self.plot_feature_importance()



#vs = Visualizer("male",10.5, 22, 30, 75)
# vs.cbc_comparison_chart()
# vs.hemoglobin_risk_indicator()
# vs.radar_chart()
# vs.plot_prediction_probability()
#vs.plot_feature_importance()



# if __name__ == "__main__":

#     generate_medical_report(
#         patient_id="P001",
#         name="John Doe",
#         age=35,
#         gender="Male",
#         hb=9,
#         mch=22,
#         mchc=30,
#         mcv=75,
#         prediction="Anemia Detected",
#         risk="Moderate",
#         anemia_type="Microcytic"
#     )
