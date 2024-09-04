from features import home_page_feature
from features import resume_optimization_feature, job_search_assistance
import streamlit as st
import os
from utils import (social_media,
                   template_end,
                   footer, 
                   page_config,
                   style_app)
from dotenv import load_dotenv

load_dotenv()

page_config()
style_app()

openai_api_key = os.getenv('OPENAI_API_KEY')
lyzr_x_key = os.getenv('X_API_Key')
serp_api_key = os.getenv('SERP_KEY')


image = "./src/logo/lyzr-logo.png"
st.sidebar.image(image=image)
social_media(justify="space-evenly")
st.sidebar.markdown("---")
st.sidebar.subheader("Virtual Career Mentor")


# Initialize session state for active page
if 'active_page' not in st.session_state:
    st.session_state.active_page = "Home"

# Function to handle button clicks
def set_page(page_name):
    st.session_state.active_page = page_name

if st.sidebar.button("Home", key="home_button"):
    set_page("Home")


# Create two columns for the buttons
col1, col2 = st.sidebar.columns(2, gap="small")  # Adding a small gap between columns


# Place buttons in the first column
with col1:
    if st.button("Resume", key="resume_button"):
        set_page("Resume Optimization")
    # if st.button("Performance", key="performance_button"):
    #     set_page("Performance Management")
    

# Place buttons in the second column
with col2:
    if st.button("Job Search", key="jobsearch_button"):
        set_page("Job Search Assistance")
    # if st.button("Development", key="learning_button"):
    #     set_page("Learning & Development")
    

# Navigate to respective pages based on session state
if st.session_state.active_page == "Home":
    home_page_feature()
elif st.session_state.active_page == "Resume Optimization":
    resume_optimization_feature(OPENAI_API_KEY=openai_api_key, LYZR_X_KEY=lyzr_x_key)
elif st.session_state.active_page == "Job Search Assistance":
    job_search_assistance(OPENAI_API_KEY=openai_api_key, LYZR_X_KEY=lyzr_x_key, SERP_API_KEY=serp_api_key)
# elif st.session_state.active_page == "Performance Management":
#     PerformanceManagement(OPENAI_API_KEY=openai_api_key, LYZR_X_KEY=lyzr_x_key)
# elif st.session_state.active_page == "Learning & Development":
#     LearningDevelopment(OPENAI_API_KEY=openai_api_key, LYZR_X_KEY=lyzr_x_key)
# elif st.session_state.active_page == "Employee Engagement":
#     EmployeeEngagement()
# elif st.session_state.active_page == "Compliance & Reporting":
#     ComplianceReporting()

# sidebar
st.markdown('---')
st.sidebar.markdown('---')
template_end()


# Footer
# footer()