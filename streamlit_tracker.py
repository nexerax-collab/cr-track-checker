import streamlit as st
from datetime import datetime, timezone
import os

def get_user_info():
    """Get user info from environment or defaults"""
    return {
        'username': os.environ.get('GITHUB_USER', 'nexerax-collab'),
        'login_type': os.environ.get('LOGIN_TYPE', 'remote'),
        'access_level': os.environ.get('ACCESS_LEVEL', 'admin'),
        'department': os.environ.get('DEPARTMENT', 'Engineering'),
    }

def format_timestamp():
    """Get formatted UTC timestamp"""
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# Initialize session state
if 'user_info' not in st.session_state:
    st.session_state.user_info = get_user_info()
if 'login_time' not in st.session_state:
    st.session_state.login_time = format_timestamp()

st.set_page_config(page_title="🚀 Fast-Track CCB Evaluation", layout="centered")

# Updated styling with white background and blue/green/yellow accents
st.markdown("""
    <style>
    /* Main button styling */
    .stButton > button {
        background-color: #2196F3;  /* Blue accent */
        color: white;
        font-weight: bold;
        padding: 0.5em 2em;
        border-radius: 10px;
        border: none;
        margin-top: 1em;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #1976D2;  /* Darker blue on hover */
    }
    
    /* Metadata box styling */
    .metadata-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Grid layout for metadata */
    .metadata-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    
    /* Text styling */
    .small-text {
        font-size: 0.85em;
        color: #666;
        margin-bottom: 0.2rem;
    }
    
    .value-text {
        color: #2196F3;  /* Blue accent */
        font-weight: 500;
    }
    
    /* Status indicators */
    .status-active {
        color: #4CAF50;  /* Green accent */
        font-weight: 500;
    }
    
    .status-warning {
        color: #FFC107;  /* Yellow accent */
        font-weight: 500;
    }
    
    /* Custom header styling */
    .custom-header {
        color: #2196F3;  /* Blue accent */
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    /* Form section styling */
    .form-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #E0E0E0;
    }
    
    /* Radio and checkbox custom colors */
    .stRadio > label {
        color: #2196F3 !important;  /* Blue accent */
    }
    
    /* Slider custom colors */
    .stSlider > div > div > div {
        background-color: #2196F3 !important;  /* Blue accent */
    }
    
    /* Success message styling */
    .success-message {
        background-color: #4CAF50;  /* Green accent */
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Warning message styling */
    .warning-message {
        background-color: #FFC107;  /* Yellow accent */
        color: #333;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Updated metadata display
st.markdown(f"""
<div class="metadata-box">
    <div class="metadata-grid">
        <div>
            <div class="small-text">Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted):</div>
            <div class="value-text">{format_timestamp()}</div>
        </div>
        <div>
            <div class="small-text">Current User's Login:</div>
            <div class="value-text">{st.session_state.user_info['username']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("🚀 Fast-Track CCB Change Evaluation")
st.markdown("Use this smart form to quickly assess whether a software change request qualifies for fast-track approval.")

with st.form("change_form"):
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.header("🔍 Change Request Details")
    
    cr_id = st.text_input("**Change Request ID/Title:**", 
                         placeholder="Enter CR ID or title...")

    description = st.text_area("**Change Description:**", 
                             placeholder="Briefly describe the proposed change...",
                             height=100)

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
    st.caption("Consider: Code complexity, dependencies, and potential side effects")
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
    st.caption("Include development, testing, and deployment costs")
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

    st.markdown("**Urgency / Vehicle Launch Impact:**")
    st.caption("Consider impact on project timeline and deliverables")
    urgency = st.radio(
        "Select urgency level",
        options=["critical", "important", "nice_to_have"],
        format_func=lambda x: {
            "critical": "Needed to meet release date",
            "important": "Important but not release-blocking",
            "nice_to_have": "Nice to have"
        }[x]
    )

    st.markdown("**Supporting Documents (Optional):**")
    uploaded_files = st.file_uploader("Upload relevant documents", 
                                    accept_multiple_files=True)

    submit = st.form_submit_button("Evaluate Change")

if submit:
    score = 0
    
    if not cr_id.strip():
        st.error("Please enter a Change Request ID/Title")
    elif not description.strip():
        st.error("Please provide a Change Description")
    else:
        # Scoring logic (same as before)
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
        
        with st.expander("Review Change Details"):
            st.markdown(f"**Change Request ID/Title:** {cr_id}")
            st.markdown(f"**Description:** {description}")
            st.markdown(f"**Estimated Cost:** {cost:,} EUR")
            st.markdown(f"**Technical Risk:** {technical_risk}")
            st.markdown(f"**Teams Involved:** {teams_involved}")
        
        if score <= 4:
            st.markdown('<div class="success-message">', unsafe_allow_html=True)
            st.success("✅ This change is likely suitable for fast-track approval.")
            st.markdown("🚀 Fast-track approved!")
            st.markdown("""
                ### Next Steps:
                1. Document the change in the CCB tracking system
                2. Notify relevant stakeholders
                3. Proceed with implementation
            """)
        elif 5 <= score <= 8:
            st.markdown('<div class="warning-message">', unsafe_allow_html=True)
            st.warning("⚠️ This change may need additional review before fast-track approval.")
            st.markdown("""
                ### Recommended Actions:
                1. Review risk mitigation strategies
                2. Consider breaking down the change into smaller parts
                3. Consult with technical leads
            """)
        else:
            st.error("❌ This change likely requires full CCB review.")
            st.markdown("""
                ### Required Actions:
                1. Schedule a full CCB review
                2. Prepare detailed documentation
                3. Consider impact analysis
            """)

        st.caption("Scoring based on best practices from regulated industries.")
        
        with st.expander("View Scoring Breakdown"):
            st.markdown("""
                ### Score Components:
                - Scope Impact: +2 if multiple systems affected
                - Safety Impact: +5 if safety/compliance affected
                - Technical Risk: 0-4 points based on complexity
                - Test Coverage: 0-4 points based on test status
                - Cost Impact: +2 if over 20,000 EUR
                - Teams Involved: 0-4 points based on number of teams
                - Urgency: -1 if critical for release
            """)

if not submit:
    with st.expander("ℹ️ How to use this form"):
        st.markdown("""
            1. Fill in all required fields
            2. Provide accurate estimates and assessments
            3. Upload any supporting documents
            4. Click 'Evaluate Change' to get the result
            
            The evaluation considers multiple factors to determine if the change
            qualifies for fast-track approval or requires full CCB review.
        """)
