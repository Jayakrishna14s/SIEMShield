import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

# Database Configuration
DB_CONFIG = {
    "dbname": "SIEMSHIELD",
    "user": "Jayakrishna",
    "password": "root",
    "host": "postgres",
    "port": "5432",
}

# Cached DB Connection
@st.cache_resource
def get_connection():
    return psycopg2.connect(cursor_factory=RealDictCursor, **DB_CONFIG)

# Fetch Data
def fetch_threats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM THREATS ORDER BY timestamp DESC;")
    return cursor.fetchall()

def fetch_suggestions(threat_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT suggestion FROM SUGGESTIONS WHERE threat_id = %s;", (threat_id,))
    return [row["suggestion"] for row in cursor.fetchall()]

# Dynamic Threat Type
def get_threat_type(threat_id):
    return "SQL Injection" if threat_id == 1 else "Brute Force"

# HTML + CSS Styling
def inject_custom_css():
    st.markdown("""
    <style>
    .threat-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border-left: 5px solid #FF4B4B;
    }
    .threat-card:hover {
        transform: scale(1.01);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
    }
    .threat-header {
        font-weight: 600;
        font-size: 18px;
        margin-bottom: 8px;
    }
    .threat-meta {
        font-size: 14px;
        color: #666666;
        margin-bottom: 12px;
    }
    .suggestion-box {
        background-color: #f1f1f1;
        padding: 10px 16px;
        margin-top: 10px;
        border-radius: 10px;
    }
    .suggestion-item {
        margin-bottom: 8px;
    }
    /* Hide Streamlit Default Menu */
    #MainMenu, header, footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# App Layout
st.set_page_config(page_title="Threat Intelligence", layout="centered")
inject_custom_css()
st.title("🛡️ Threat Detection Dashboard")

threats = fetch_threats()

if not threats:
    st.info("✅ No threats detected.")
else:
    for threat in threats:
        threat_type = get_threat_type(threat["threat_id"])
        summary = f"{threat_type} attempt by **{threat['ip']}** at **{threat['timestamp']}**"
        toggle_key = f"toggle_{threat['id']}"

        with st.container():
            st.markdown(f"<div class='threat-header'>🚨 {threat_type} Detected</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='threat-meta'>{summary}</div>", unsafe_allow_html=True)

            show_suggestions = st.toggle("💡 Show Suggestions", key=toggle_key)
            if show_suggestions:
                suggestions = fetch_suggestions(threat["threat_id"])
                # st.markdown("<div class='suggestion-box'>", unsafe_allow_html=True)
                st.markdown("**💬 Recommendations:**")
                for s in suggestions:
                    st.markdown(f"<div class='suggestion-item'>• {s}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
