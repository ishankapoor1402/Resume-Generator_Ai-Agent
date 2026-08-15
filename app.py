import streamlit as st
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Resume Generator",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# SIDEBAR - API KEYS
# =========================================================

st.sidebar.title("🔑 API Keys")

GOOGLE_API_KEY = st.sidebar.text_input(
    "Google API Key",
    type="password",
    placeholder="Paste your Google API key here"
)

GROQ_API_KEY = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="Paste your Groq API key here"
)


# =========================================================
# CHECK GOOGLE API KEY
# =========================================================

if not GOOGLE_API_KEY:
    st.warning("Please Provide API Key For Google!!")
    st.stop()


# =========================================================
# GOOGLE GEMINI MODEL
# =========================================================

try:

    model1 = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=GOOGLE_API_KEY
    )

except Exception as e:

    st.error("❌ Google Gemini initialization failed.")
    st.exception(e)
    st.stop()


# =========================================================
# GROQ MODEL
# =========================================================

model2 = None

if GROQ_API_KEY:

    try:

        model2 = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=GROQ_API_KEY
        )

    except Exception as e:

        st.warning("⚠️ Groq model could not be initialized.")
        st.exception(e)


# =========================================================
# MAIN APP
# =========================================================

st.title("📄 AI Resume Generator")

st.write(
    "Generate professional resume content using Google Gemini."
)


# =========================================================
# USER INPUT
# =========================================================

name = st.text_input("Full Name")

email = st.text_input("Email")

phone = st.text_input("Phone Number")

education = st.text_area(
    "Education",
    placeholder="Example: BCA, IITM IPU"
)

skills = st.text_area(
    "Skills",
    placeholder="Example: Python, Generative AI, LangChain, AWS, Groq"
)

experience = st.text_area(
    "Experience",
    placeholder="Enter your work experience..."
)

projects = st.text_area(
    "Projects",
    placeholder="Enter your projects..."
)


# =========================================================
# GENERATE RESUME
# =========================================================

if st.button("🚀 Generate Resume"):

    if not name:
        st.error("Please enter your name.")
        st.stop()

    prompt = f"""
Create a professional resume for the following candidate.

Name:
{name}

Email:
{email}

Phone:
{phone}

Education:
{education}

Skills:
{skills}

Experience:
{experience}

Projects:
{projects}

Create a clean, professional and ATS-friendly resume.

Use these sections:

1. Professional Summary
2. Education
3. Technical Skills
4. Experience
5. Projects
6. Achievements
7. Certifications

Do not invent fake information.
If information is missing, simply leave that section empty.
"""


    # =====================================================
    # CALL GEMINI
    # =====================================================

    try:

        with st.spinner("Generating your resume..."):

            response = model1.invoke(prompt)

        st.success("✅ Resume Generated Successfully!")

        st.markdown("## 📄 Generated Resume")

        st.write(response.content)

    except Exception as e:

        st.error("❌ Gemini API Error")

        st.exception(e)
