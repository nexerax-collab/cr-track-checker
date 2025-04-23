import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="🚀 Fast-Track CCB Evaluation", layout="centered")
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5em 2em;
        border-radius: 10px;
        border: none;
        margin-top: 1em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Fast-Track CCB Change Evaluation")
st.markdown("Use this smart form to quickly assess whether a software change request qualifies for fast-track approval.")

with st.form("change_form"):
    st.header("🔍 Change Request Details")

    scope = st.radio("**Scope of Impact:**", [
        "Isolated to one component/module",
        "Affects multiple systems/modules"
    ])

    safety = st.radio("**Safety & Compliance Impact:**", [
        "No safety or compliance impact",
        "Possible impact on safety or regulations"
    ])

    technical_risk = st.selectbox("**Technical Risk & Complexity:**", [
        "Very low (well-known fix, low complexity)",
        "Moderate (minor new logic)",
        "High (novel or critical logic change)"
    ])

    test_coverage = st.radio("**Testing & Validation:**", [
        "Fully tested (unit + integration)",
        "Partially tested",
        "Not tested"
    ])

    cost = st.slider("**Estimated Change Cost (€):**", 0, 20000, 1000, step=100)

    teams_involved = st.selectbox("**Teams Involved:**", [
        "1 team",
        "2-3 teams",
        "More than 3 or external vendor"
    ])

    urgency = st.radio("**Urgency / Vehicle Launch Impact:**", [
        "Needed to meet release date",
        "Important but not release-blocking",
        "Nice to have"
    ])

    submit = st.form_submit_button("Evaluate Change")

if submit:
    score = 0
    if scope == "Isolated to one component/module":
        score += 0
    else:
        score += 2

    if safety == "No safety or compliance impact":
        score += 0
    else:
        score += 5

    risk_scores = {
        "Very low (well-known fix, low complexity)": 0,
        "Moderate (minor new logic)": 2,
        "High (novel or critical logic change)": 4
    }
    score += risk_scores[technical_risk]

    test_scores = {
        "Fully tested (unit + integration)": 0,
        "Partially tested": 2,
        "Not tested": 4
    }
    score += test_scores[test_coverage]

    if cost > 5000:
        score += 2

    team_scores = {
        "1 team": 0,
        "2-3 teams": 2,
        "More than 3 or external vendor": 4
    }
    score += team_scores[teams_involved]

    if urgency == "Needed to meet release date":
        score -= 1

    st.header("🧮 Evaluation Result")
    if score <= 4:
        st.success("✅ This change is likely suitable for fast-track approval.")
        rain(emoji="🚀", font_size=28, falling_speed=5, animation_length="short")
    elif 5 <= score <= 8:
        st.warning("⚠️ This change may need additional review before fast-track approval.")
    else:
        st.error("❌ This change likely requires full CCB review.")

    st.caption("Scoring based on best practices from regulated industries.")
