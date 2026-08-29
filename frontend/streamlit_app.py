import os
import base64
from pathlib import Path

import requests
import streamlit as st


# --------------------------------------------------
# API configuration
# --------------------------------------------------

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8001"
)


# --------------------------------------------------
# Background image
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKGROUND_IMAGE = PROJECT_ROOT / "assets" / "background.jpg"


def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()


background_base64 = get_base64_image(BACKGROUND_IMAGE)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    f"""
    <style>

    /* ------------------------------
       Page background
    ------------------------------ */

    .stApp {{
        background:
            linear-gradient(
                rgba(25, 18, 10, 0.20),
                rgba(25, 18, 10, 0.25)
            ),
            url("data:image/jpeg;base64,{background_base64}");

        background-size: cover;
        background-position: center 35%;
        background-attachment: fixed;
    }}


    /* ------------------------------
       Main glass panel
    ------------------------------ */

    .main .block-container {{
        background: rgba(255, 255, 255, 0.12);

        border: 1px solid rgba(255, 255, 255, 0.20);
        border-radius: 28px;

        padding: 2.5rem 3rem !important;

        max-width: 850px;

        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);

        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.12);
    }}


    /* ------------------------------
       Hero card
    ------------------------------ */

    .hero {{
        background: rgba(20, 15, 8, 0.20);

        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 24px;

        padding: 1rem 2.5rem;
        margin-bottom: 2rem;

        text-align: center;

        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.25);
    }}

    .hero h1 {{
        color: #fff8e7 !important;

        font-size: 2.5rem;
        font-weight: 750;

        margin-top: 0;
        margin-bottom: 0.8rem;

        text-shadow:
            0 2px 6px rgba(0, 0, 0, 0.55);
    }}

    .hero p {{
        color: rgba(255, 255, 255, 0.92) !important;

        font-size: 1.05rem;
        line-height: 1.6;

        max-width: 650px;
        margin: 0 auto;

        text-shadow:
            0 1px 4px rgba(0, 0, 0, 0.50);
    }}


    /* ------------------------------
       Main headings
    ------------------------------ */

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {{
        color: #263a2e !important;
        text-shadow: none !important;
    }}


    /* ------------------------------
       Standard text
    ------------------------------ */

    [data-testid="stMarkdownContainer"] p {{
        color: #334139 !important;
        text-shadow: none !important;
    }}


    /* ------------------------------
       Metric
    ------------------------------ */

    [data-testid="stMetric"] {{
        background: rgba(246, 250, 247, 0.92);

        border: 1px solid rgba(46, 107, 60, 0.15);
        border-radius: 16px;

        padding: 1rem 1.2rem;
    }}

    [data-testid="stMetricLabel"] p {{
        color: #58675e !important;
        text-shadow: none !important;
    }}

    [data-testid="stMetricValue"] {{
        color: #25382c !important;
    }}


    /* ------------------------------
       Buttons
    ------------------------------ */

    .stButton > button {{
        width: 100%;

        background: #2f6b3c !important;
        color: white !important;

        border: none !important;
        border-radius: 12px !important;

        font-weight: 600 !important;

        transition: 0.2s ease;
    }}

    .stButton > button p {{
        color: white !important;
        text-shadow: none !important;
    }}

    .stButton > button:hover {{
        background: #255832 !important;
        color: white !important;

        transform: translateY(-1px);

        box-shadow:
            0 6px 16px rgba(0, 0, 0, 0.22);
    }}


    /* ------------------------------
       Divider
    ------------------------------ */

    hr {{
        border-color: rgba(38, 58, 46, 0.15) !important;
    }}


    /* ------------------------------
       Small helper / caption text
       Keep these near the end so they
       override general text rules
    ------------------------------ */

    [data-testid="stCaptionContainer"] p {{
        color: #ffffff !important;

        font-weight: 500 !important;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.90),
            0 2px 6px rgba(0, 0, 0, 0.55) !important;
    }}


    /* ------------------------------
       Input / uploader labels
    ------------------------------ */

    [data-testid="stWidgetLabel"] p {{
        color: #ffffff !important;

        font-weight: 600 !important;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.90),
            0 2px 6px rgba(0, 0, 0, 0.55) !important;
    }}


    /* ------------------------------
       Uploaded image caption
    ------------------------------ */

    [data-testid="stImage"] figcaption {{
        color: #ffffff !important;

        font-weight: 500 !important;

        text-shadow:
            0 1px 3px rgba(0, 0, 0, 0.90);
    }}

    /* ------------------------------
        Diagnosis result card
    ------------------------------ */

    .diagnosis-result {{
        background: rgba(255, 255, 255, 0.92);

        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 14px;

        padding: 1rem 1.3rem;
        margin-bottom: 1rem;

        color: #1f2d24 !important;

        font-size: 1.15rem;
        font-weight: 650;

        text-shadow: none !important;

        box-shadow:
            0 6px 18px rgba(0, 0, 0, 0.10);

        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }}


    /* ------------------------------
    Answer card
    ------------------------------ */

    .answer-result {{
        background: rgba(255, 255, 255, 0.92);

        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 14px;

        padding: 1.2rem 1.4rem;
        margin-top: 0.5rem;

        color: #1f2d24 !important;

        font-size: 1rem;
        line-height: 1.8;

        text-shadow: none !important;

        box-shadow:
            0 6px 18px rgba(0, 0, 0, 0.10);

        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Hero
# --------------------------------------------------

st.markdown(
    """
<div class="hero">
<h1>Plant Disease Diagnosis Assistant</h1>
<p>Upload a plant leaf image to predict a possible disease and ask questions about symptoms, causes, treatment, and prevention.</p>
</div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Image upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a leaf image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded leaf image"
    )

    if st.button("Predict Disease"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        try:
            response = requests.post(
                f"{API_URL}/predict",
                files=files,
                timeout=60
            )

            if response.status_code == 200:

                result = response.json()

                # Save the prediction across Streamlit reruns
                st.session_state["prediction"] = result

                # Clear previous answer when a new prediction is made
                st.session_state.pop("answer", None)

            else:
                st.error(
                    f"Prediction failed "
                    f"(HTTP {response.status_code})."
                )

        except requests.RequestException as error:
            st.error(
                f"Could not connect to the prediction API: {error}"
            )


# --------------------------------------------------
# Prediction result
# --------------------------------------------------

if "prediction" in st.session_state:

    result = st.session_state["prediction"]

    disease_name = (
        result["class_name"]
        .replace("___", " - ")
        .replace("_", " ")
    )

    st.subheader("Diagnosis")

    st.markdown(
        f"""
    <div class="diagnosis-result">
    {disease_name}
    </div>
        """,
        unsafe_allow_html=True
    )

    st.metric(
        label="Confidence",
        value=f"{result['confidence']:.2%}"
    )

    st.divider()


    # --------------------------------------------------
    # Question answering
    # --------------------------------------------------

    st.subheader("Ask about the diagnosis")

    question = st.text_input(
        "Enter your question",
        placeholder="How can I prevent this disease?"
    )

    if st.button("Ask") and question:

        try:
            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "class_name": result["class_name"],
                    "question": question
                },
                timeout=60
            )

            if response.status_code == 200:

                answer_result = response.json()

                st.session_state["answer"] = answer_result

            else:
                st.error(
                    f"Question answering failed "
                    f"(HTTP {response.status_code})."
                )

        except requests.RequestException as error:
            st.error(
                f"Could not connect to the question-answering API: {error}"
            )


# --------------------------------------------------
# Answer
# --------------------------------------------------

if "answer" in st.session_state:

    answer_result = st.session_state["answer"]

    st.caption(
        f"Detected intent: {answer_result['intent']} "
        f"({answer_result['intent_confidence']:.1%} confidence)"
    )

    st.subheader("Answer")

    answer_html = answer_result["answer"].replace("\n", "<br>")

    st.markdown(
        f"""
    <div class="answer-result">
    {answer_html}
    </div>
        """,
        unsafe_allow_html=True
    )