import streamlit as st

st.set_page_config(page_title="🚀 Fast-Track CCB Evaluation", layout="centered")

# Updated styling with white background and blue/green/yellow accents
st.markdown("""
    <style>
    .stButton > button {
        background-color: #2196F3;
        color: white;
        font-weight: bold;
        padding: 0.5em 2em;
        border-radius: 10px;
        border: none;
        margin-top: 1em;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #1976D2;
    }
    
    div.stRadio > label {
        color: #2196F3 !important;
    }
    
    div.stSlider > div > div > div {
        background-color: #2196F3 !important;
    }
    
    .success-message {
        background-color: #4CAF50;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .warning-message {
        background-color: #FFC107;
        color: #333;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .stTitle {
        color: #2196F3;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Fast-Track CCB Evaluation")
st.markdown("Quick assessment for fast-track approval qualification")

with st.form("change_form"):
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

    st.markdown("**Technical Risk & Complexity:**")
    technical_risk = st.selectbox(
        "Select risk level",
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

    st.markdown("**Estimated Change Cost (EUR):**")
    cost = st.slider("Select cost", 0, 100000, 5000, step=1000)

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
    
    # Scoring logic
    score += 2 if scope == "multiple" else 0
    score += 5 if safety == "has_impact" else 0
    score += {"very_low": 0, "moderate": 2, "high": 4}[technical_risk]
    score += {"fully": 0, "partially": 2, "not_tested": 4}[test_coverage]
    if cost > 20000:
        score += 2
    score += {"one": 0, "two_three": 2, "more": 4}[teams_involved]
    if urgency == "critical":
        score -= 1

    st.header("🧮 Evaluation Result")
    
    # Display evaluation result
    if score <= 4:
        st.success("✅ This change is likely suitable for fast-track approval.")
        st.markdown("🚀 **Fast-track approved!**")
        st.markdown("""
            **Next Steps:**
            1. Document change in CCB system
            2. Notify stakeholders
            3. Proceed with implementation
        """)
    elif 5 <= score <= 8:
        st.warning("⚠️ This change may need additional review before fast-track approval.")
        st.markdown("""
            **Recommended Actions:**
            1. Review risk mitigation
            2. Consider smaller changes
            3. Consult technical leads
        """)
    else:
        st.error("❌ This change requires full CCB review.")
        st.markdown("""
            **Required Actions:**
            1. Schedule CCB review
            2. Prepare documentation
            3. Analyze impact
        """)

    with st.expander("View Scoring Details"):
        st.markdown(f"""
            **Final Score: {score}**
            - Scope: +2 if multiple systems
            - Safety: +5 if safety impact
            - Tech Risk: 0-4 points
            - Testing: 0-4 points
            - Cost: +2 if >20,000 EUR
            - Teams: 0-4 points
            - Urgency: -1 if critical
        """)

if not submit:
    with st.expander("ℹ️ Quick Guide"):
        st.markdown("""
            1. Assess each category
            2. Use accurate estimates
            3. Click 'Evaluate Change'
            
            Score ≤4: Fast-track eligible
            Score 5-8: Needs review
            Score >8: Full CCB required
        """)
