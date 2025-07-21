import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")  # Ensure this file is in your project folder
    firebase_admin.initialize_app(cred)

# Streamlit page settings
st.set_page_config(
    page_title="Personalized Women's Healthcare Assistant",
    layout="wide",
)

# Ensure session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# User Login/Signup Page with Firebase
def login_page():
    st.title("👩‍⚕️ Personalized Women's Healthcare Assistant Login")
    
    tab1, tab2 = st.tabs(["Login", "Signup"])

    # Login
    with tab1:
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Password", type="password", key="login_pass")

        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"✅ Logged in as {email}")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Login failed: {e}")

    # Signup
    with tab2:
        new_email = st.text_input("📧 Enter Email", key="signup_email")
        new_password = st.text_input("🔑 Enter Password", type="password", key="signup_pass")

        if st.button("Sign Up"):
            try:
                user = auth.create_user(email=new_email, password=new_password)
                st.success("✅ Signup successful! You can now log in.")
            except Exception as e:
                st.error(f"❌ Signup failed: {e}")

# Display login page if user is not authenticated
if not st.session_state.logged_in:
    login_page()
else:
    st.title("🩺 Personalized Women's Healthcare Assistant")

    # Logout option
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.experimental_rerun()

    # Main App Content
    tab1, tab2 = st.tabs(["Health Assessment", "Personalized Recommendations"])

    with tab1:
        st.subheader("📋 Provide Your Health Information")
        age = st.number_input("Age", min_value=10, max_value=100, step=1)
        lifestyle = st.selectbox("Lifestyle", ["Sedentary", "Moderate Activity", "Highly Active"])
        health_goals = st.text_input("Your Health Goals (e.g., weight loss, hormonal balance, pregnancy planning)")
        medical_conditions = st.text_area("Any existing medical conditions or concerns")
        dietary_preferences = st.text_input("Dietary Preferences (e.g., vegetarian, gluten-free, no restrictions)")

        if st.button("Analyze Health Profile"):
            st.subheader("💡 Personalized Health Recommendations:")
            st.write(f"- Age: {age}\n- Lifestyle: {lifestyle}\n- Health Goals: {health_goals}\n- Conditions: {medical_conditions}\n- Diet: {dietary_preferences}")

    with tab2:
        st.subheader("🌿 General Wellness Tips for Women")
        st.markdown(
            """
            - 🥗 **Balanced Nutrition**: Include a variety of fruits, vegetables, and lean proteins.
            - 🚴 **Stay Active**: Engage in regular physical activity like yoga, walking, or strength training.
            - 💧 **Hydration**: Drink at least 8 glasses of water daily.
            - 😴 **Rest Well**: Ensure 7-9 hours of quality sleep per night.
            - 🏥 **Routine Checkups**: Regular gynecological exams and screenings are crucial.
            - 🧘 **Mental Well-being**: Manage stress with meditation, hobbies, and social connections.
            """
        )
