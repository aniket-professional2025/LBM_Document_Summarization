# Importing required packages
import streamlit as st
import json
from io import StringIO
from main import generate_summary

# Load user profiles from JSON
with open(r"C:\Users\Webbies\Jupyter_Notebooks\Assessli_LBM\user_profile.json", "r") as f:
    user_profiles = json.load(f)

# Set Streamlit page configuration
st.set_page_config(page_title="User-Aware Summarizer", layout="wide")

# Page Title
st.title("📘 LBM Document Summarizer with User Profiles")

st.markdown("""
Upload a document, select a user profile, and get a personalized summary based on the user's focus, tone, and preferences.
""")

st.markdown("---")

# File Upload Section
uploaded_file = st.file_uploader("📤 Upload a Text Document", type=["txt"])

document_text = ""
if uploaded_file is not None:
    # Read uploaded text
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    document_text = stringio.read()
    st.subheader("📝 Uploaded Document Preview")
    st.text_area("Document Content", document_text, height=200)

# Sidebar: User Selection
st.sidebar.header("👤 Select User Profile")

# Add a restart session button at the top of the sidebar
if st.sidebar.button("🔄 Restart Session"):
    st.session_state.clear()  
    st.rerun()   

# Default option as instruction text
user_choice = st.sidebar.selectbox(
    "Choose a user:",
    options=["Click here to choose user profile"] + list(user_profiles.keys()),
    index=0
)

user_profile = None

if user_choice != "Click here to choose user profile":
    user_profile = user_profiles[user_choice]

    # Display the selected user’s profile
    st.sidebar.markdown("### User Preferences")
    st.sidebar.markdown(f"**Focus:** {user_profile['focus']}")
    st.sidebar.markdown(f"**Tone:** {user_profile['tone']}")
    st.sidebar.markdown(f"**Length:** {user_profile['length']}")
    st.sidebar.markdown("**History:**")
    for item in user_profile["history"]:
        st.sidebar.write(f"- {item}")
else:
    st.sidebar.info("Please choose a user profile from the dropdown.")

st.markdown("---")

# Dynamic button label based on selected user
if user_choice != "Click here to choose user profile":
    button_label = f"🚀 Generate summary from {user_choice.replace('_', ' ').title()} perspective"
else:
    button_label = "🚀 Generate Personalized Summary"

if st.button(button_label):
    if not uploaded_file:
        st.error("Please upload a document first.")
    elif user_choice == "Click here to choose user profile":
        st.error("Please select a user profile.")
    else:
        with st.spinner("Generating summary... Please wait."):
            try:
                # Call the summary generation function
                summary = generate_summary(document_text, user_profile)
                st.success("✅ Summary Generated Successfully!")
                st.subheader("🧠 Personalized Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error during summary generation: {e}")