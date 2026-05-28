# AI Enabled BMI Calculator – Streamlit App (`app.py`)

import streamlit as st
from google import genai

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI BMI Calculator",
    page_icon="⚕️",
    layout="centered"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("⚕️ AI Enabled BMI Calculator")
st.write("Calculate your BMI and get AI-generated health insights.")

# --------------------------------------------------
# API KEY
# --------------------------------------------------
google_api_key=st.secrets["google"]["api_key"]

c=genai.Client(api_key=google_api_key)
# --------------------------------------------------
# USER INPUTS
# --------------------------------------------------
height = st.number_input(
    "Enter your height (in meters)",
    min_value=0.5,
    max_value=3.0,
    value=1.70,
    step=0.01
)

weight = st.number_input(
    "Enter your weight (in kg)",
    min_value=10.0,
    max_value=300.0,
    value=70.0,
    step=0.1
)

# --------------------------------------------------
# BMI CALCULATION FUNCTION
# --------------------------------------------------
def calculate_bmi(height, weight):
    bmi = round(weight / (height ** 2), 2)

    if bmi <= 18.5:
        category = "Underweight"
    elif bmi <= 24.9:
        category = "Healthy"
    elif bmi <= 29.9:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category

# --------------------------------------------------
# BUTTON ACTION
# --------------------------------------------------
if st.button("Calculate BMI"):

    bmi, category = calculate_bmi(height, weight)

    # Display BMI Result
    st.subheader("BMI Result")
    st.metric(label="Your BMI", value=bmi)
    st.success(f"Category: {category}")

    # --------------------------------------------------
    # AI HEALTH INSIGHTS
    # --------------------------------------------------
    with st.spinner("Generating AI health insights..."):

        prompt = f"""
        My BMI is {bmi} and my category is {category}.

        Give:
        1. 5 short health insights
        2. Diet suggestions
        3. Exercise recommendations
        4. Lifestyle improvement tips

        Keep the response beginner friendly.
        """

        try:
            response = c.models.generate_content(model="gemini-2.5-flash",contents = prompt)

            st.subheader("🤖 AI Health Insights")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error generating AI response: {e}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption("Built with Streamlit + Google Gemini AI")