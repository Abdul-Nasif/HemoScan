import streamlit as st
from train_model import  AnemiaPredictor
from visuals import Visualizer
from pdf_genarator import generate_medical_report
import random
import os
st.markdown("<h1 style='text-align: center; color: #487531; font-family: Arial sans-serif;text-shadow: 2px 2px 4px rgba(0,0,0,0.1);letter-spacing: 2px;'>HemoScan - Blood Analysis System</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #32CD32;font-family: Arial sans-serif;text-shadow: 1px 1px 2px rgba(0,0,0,0.1);letter-spacing: 2px;'>Powered by Oiron</h5>", unsafe_allow_html=True)

# -----------------------------
# User Details Form
# -----------------------------

if "user_submitted" not in st.session_state:
    st.session_state.user_submitted = False

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result= None
st.header("User Details")


with st.form("user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    submit_user = st.form_submit_button("Save Details")

    if submit_user:
        if name =="" or age == 0 or gender == "":
            st.error("Please fill in all details")
            submit_user = False
            st.session_state.user_submitted = False
        else:
            st.session_state.user_submitted = True
            st.success("User details saved")

# -----------------------------
# Blood Parameter Form
# -----------------------------
if "blood_submitted" not in st.session_state:
    st.session_state.blood_submitted = False
st.header("Blood Parameters")
with st.form("blood_form"):

    col1, col2 = st.columns(2)
    with col1: 
        hb = st.number_input("Hemoglobin (Hb)")
    with col2:
        hb_unit = st.selectbox("Hb Unit", ["g/dL", "g/L"])
    col3, col4 = st.columns(2)
    with col3:
        mch = st.number_input("MCH")
    with col4:
        mch_unit = st.selectbox("MCH Unit", ["pg", "fg"])
    col5, col6 = st.columns(2)
    with col5:
        mchc = st.number_input("MCHC")
    with col6:
        mchc_unit = st.selectbox("MCHC Unit", ["g/dL", "g/L"])
    col7, col8 = st.columns(2)
    with col7:
        mcv = st.number_input("MCV")
    with col8:
        mcv_unit = st.selectbox("MCV Unit", ["fL"])

    submit_blood = st.form_submit_button("Submit Values")

    if submit_blood:
        if hb == 0 or mch == 0 or mchc == 0 or mcv == 0:
            st.error("Please enter all blood values")
            submit_blood = False
            st.session_state.blood_submitted = False
        else:
            st.session_state.blood_submitted = True
            st.success("Blood values submitted")

# -----------------------------
# Unit Conversion Button
# -----------------------------


# converter of unites
def convert_to_standard(hb, hb_unit, mch, mch_unit, mchc, mchc_unit, mcv, mcv_unit):

    # Hb conversion
    if hb_unit == "g/L":
        hb = hb / 10

    # MCH conversion
    if mch_unit == "fg":
        mch = mch / 1000

    # MCHC conversion
    if mchc_unit == "g/L":
        mchc = mchc / 10

    # MCV usually already fL
    if mcv_unit == "L":
        mcv = mcv * 1e15

    return hb, mch, mchc, mcv
if submit_blood:

    hb, mch, mchc, mcv = convert_to_standard(
        hb, hb_unit,
        mch, mch_unit,
        mchc, mchc_unit,
        mcv, mcv_unit
    )

    st.success("Values processed successfully")

    st.write("Standardized Values Sent to Model:")

    st.write("Hb:", hb, "g/dL")
    st.write("MCH:", mch, "pg")
    st.write("MCHC:", mchc, "g/dL")
    st.write("MCV:", mcv, "fL")

# Predict using the model
if st.session_state.user_submitted and st.session_state.blood_submitted:

    if st.button("Predict Anemia", type="primary"):

        with st.spinner("Running analysis..."):

            prediction = AnemiaPredictor()  
            result = prediction.predict(gender, hb, mch, mchc, mcv)
            st.session_state.prediction_result= result

            visual = Visualizer(gender, hb, mch, mchc, mcv)
            visual.pipline_visual()


if st.session_state.prediction_result is not None:
    result =st.session_state.prediction_result
    
    st.divider()
    with st.container(border = True):
        st.markdown(
        """
        <div style="background-color:#1f4e79;padding:10px;border-radius:8px">
        <h3 style="color:white;text-align:center;">Anemia Prediction Report</h3>
        </div>
        """,
        unsafe_allow_html=True
        )        
        st.markdown('''
        <style>
            [data-testid="stMetricLabel"] {

                color: #487531;
                font-weight: bold;
                font-family: Arial, sans-serif;
            }
            [data-testid="stMetricValue"] {

                color: #32CD32;
                font-weight: bold;
                font-family: Arial, sans-serif;
            }
        </style>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label ="Diagnosis", value=result["Diagnosis"])

        with col2:
            st.metric(label="Risk Probability", value=result["Risk"])
        with col3:
            st.metric(label="Type", value=result["Type"])


        st.info(f"Recommendation: {result['Recommendation']}")


        st.divider()
        try:
            st.markdown(
                """
                <div style="background-color:#1f4e79;padding:10px;border-radius:8px">
                <h3 style="color:white;text-align:center;">Blood Report Visual Analysis</h3>
                </div>
                """,
                unsafe_allow_html=True
                )

            with st.container(border=True):

                col1, col2 = st.columns(2)

                with col1:
                    st.image(
                        "reports/cbc_comparison_chart.png",
                        caption="CBC Parameter Comparison",
                        width='stretch'
                    )
                    st.caption("Comparison of patient CBC values against normal reference ranges.")

                with col2:
                    st.image(
                        "reports/cbc_radar_chart.png",
                        caption="CBC Radar Analysis",
                        width='stretch'
                    )
                    st.caption("Radar visualization highlighting deviations in blood parameters.")

                st.divider()

                st.image(
                    "reports/hemoglobin_risk_indicator.png",
                    caption="Hemoglobin Risk Indicator",
                    width='stretch'
                )

                st.caption("Visual indicator showing hemoglobin level relative to anemia risk thresholds.")

        except FileNotFoundError:
            st.error("Visual analysis not available. Please ensure the model generates these visualizations.")
else:
    st.warning("⚠️ Please submit both User Details and Blood Details first.")

# pdf geretor and dowmload
if st.session_state.prediction_result is not None:
    if st.button("Generate Full Report", type="secondary"):

        with st.spinner("Generating PDF report..."):

            
            patient_id = "patient_" + str(random.randint(10000, 99999))  # This should ideally be generated or retrieved from a database
            file_path = f"reports/{patient_id}_report.pdf"
            generate_medical_report(patient_id=patient_id,name = name ,age = age,gender=gender, hb=hb, mch=mch, mchc=mchc, mcv=mcv,prediction = st.session_state.prediction_result["Diagnosis"],risk= st.session_state.prediction_result["Risk"], anemia_type= st.session_state.prediction_result["Recommendation"])
            st.success("PDF report generated successfully!")
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download Report",
                    data=f,
                    file_name=f"{patient_id}_report.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Error: Report file not found.")


if "model_probability" not in st.session_state:
    st.session_state.model_probability = False

if st.session_state.prediction_result is not None:
    st.divider()
    st.session_state.model_probability = st.button("View Model Probability Details", type="secondary")
    st.session_state.model_probability = True if st.session_state.model_probability else False
if st.session_state.model_probability:
    
    st.markdown(
        """
        <div style="background-color:#1f4e79;padding:10px;border-radius:8px">
        <h3 style="color:white;text-align:center;">Model Probability Details</h3>
        </div>
        """,
        unsafe_allow_html=True
        )

    with st.container(border=True):

        col1, col2 = st.columns(2)
        try:
            with col1:
                st.image(
                    "reports/prediction_probability.png",
                    caption="Model Probability Distribution",
                    width='stretch'
                )
                st.caption("Distribution of predicted probabilities for each anemia type.")
            with col2:
                st.image(
                    "reports/feature_importance.png",
                    caption="Feature Importance",
                    width='stretch'
                )
                st.caption("Importance of each feature in the model's prediction.")
            if st.button("Hide Probability Details", type="secondary"):
                st.session_state.model_probability = False
        except FileNotFoundError:
            st.error("Probability details not available. Please ensure the model generates these visualizations.")



