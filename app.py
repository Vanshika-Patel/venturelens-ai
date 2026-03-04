import streamlit as st
import requests

st.set_page_config(page_title="VentureLens - AI VC Evaluator")

st.title("🚀 VentureLens")
st.subheader("AI-Powered Startup Investment Simulator")

st.divider()

idea = st.text_area("Startup Idea")
industry = st.text_input("Industry")
customer = st.text_input("Target Customer")
geo = st.text_input("Geography")
revenue = st.text_input("Revenue Model")
stage = st.selectbox("Stage", ["Idea", "MVP", "Revenue"])


def query_huggingface(prompt):
    API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 800,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


if st.button("Simulate VC Decision"):

    prompt = f"""
You are a senior venture capital partner. Be analytical and structured.

Evaluate this startup:

Startup Idea: {idea}
Industry: {industry}
Target Customer: {customer}
Geography: {geo}
Revenue Model: {revenue}
Stage: {stage}

Provide:
1. Market Analysis (TAM, SAM, SOM)
2. Competitive Landscape
3. Unit Economics
4. SWOT
5. Risk Scores (Market, Execution, Regulatory, Capital Intensity + Overall 0-100)
6. Suggested Valuation Range
7. Investment Recommendation
8. Confidence Score
"""

    with st.spinner("Analyzing Startup..."):
        result = query_huggingface(prompt)

    st.divider()
    st.markdown("## 📊 VC Evaluation Report")

    if isinstance(result, list):
        st.write(result[0]["generated_text"])
    else:
        st.write(result)
