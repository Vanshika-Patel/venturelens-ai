import streamlit as st
from openai import OpenAI

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

if st.button("Simulate VC Decision"):

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior venture capital partner. Be analytical and structured."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    st.divider()
    st.markdown("## 📊 VC Evaluation Report")
    st.write(response.choices[0].message.content)
