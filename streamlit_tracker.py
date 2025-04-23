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

    # Using tuples with (value, display_text) for better control
    scope = st.radio(
        "**Scope of Impact:**",
        options=["isolated", "multiple"],
        format_func=lambda x: "Isolated to one component/module" if x == "isolated" else "Affects multiple systems/modules"
    )

    safety = st.radio(
        "**Safety & Compliance Impact:**",
        options=["no_impact", "has_impact"],
        format_func=lambda x: "No safety or compliance impact" if x == "no_impact" else "Possible impact on safety or regulations"
    )

    technical_risk = st.selectbox(
        "**Technical Risk & Complexity:**",
        options=["very_low", "moderate", "high"],
        format_func=lambda x: {
            "very_low": "Very low (well-known fix, low complexity)",
            "moderate": "Moderate (minor new logic)",
            "high": "High (novel or critical logic change)"
        }[x]
    )

    test_coverage = st.radio(
        "**Testing & Validation:**",
        options=["fully", "partially", "not_tested"],
        format_func=lambda x: {
            "fully": "Fully tested (unit + integration)",
            "partially": "Partially tested",
            "not_tested": "Not tested"
        }[x]
    )

    cost = st.slider("**Estimated Change Cost (€):**", 0, 20000, 1000, step=100)

    teams_involved = st.selectbox(
        "**Teams Involved:**",
        options=["one", "two_three", "more"],
        format_func=lambda x: {
            "one": "1 team",
            "two_three": "2-3 teams",
            "more": "More than 3 or external vendor"
        }[x]
    )

    urgency = st.radio(
        "**Urgency / Vehicle Launch Impact:**",
        options=["critical", "important", "nice_to_have"],
        format_func=lambda x: {
            "critical": "Needed to meet release date",
            "important": "Important but not release-blocking",
            "nice_to_have": "Nice to have"
        }[x]
    )

    submit = st.form_submit_button("Evaluate Change")

if submit:
    score = 0
    
    # Scope scoring
    score += 2 if scope == "multiple" else 0
    
    # Safety scoring
    score += 5 if safety == "has_impact" else 0
    
    # Technical risk scoring
    risk_scores = {
        "very_low": 0,
        "moderate": 2,
        "high": 4
    }
    score += risk_scores[technical_risk]
    
    # Test coverage scoring
    test_scores = {
        "fully": 0,
        "partially": 2,
        "not_tested": 4
    }
    score += test_scores[test_coverage]
    
    # Cost scoring
    if cost > 5000:
        score += 2
    
    # Teams scoring
    team_scores = {
        "one": 0,
        "two_three": 2,
        "more": 4
    }
    score += team_scores[teams_involved]
    
    # Urgency scoring
    if urgency == "critical":
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
