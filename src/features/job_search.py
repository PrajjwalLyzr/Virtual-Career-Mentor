import streamlit as st
import os
import json
import PyPDF2
from serpapi import GoogleSearch
from agents import job_search_agent
from lyzragentapi import data_summarizer
from utils import (file_checker,
                   get_file_name,
                   get_files_in_directory)

def job_search_assistance(OPENAI_API_KEY, LYZR_X_KEY, SERP_API_KEY):
    st.title('Job Search Assistance')
    st.markdown("##### Find the best fit job for you")

    data_file = file_checker(directoryName="DataFile")
    if len(data_file)>0:
        try:
            if 'active_button' not in st.session_state:
                st.session_state.active_button = None

            # Buttons for each process
            col1, col2= st.columns(2)
            with col1:
                if st.button('Resume Based Job Search'):
                    st.session_state.active_button = "Resume Based Job Search"
            with col2:
                if st.button('Profile Based Job Search'):
                    st.session_state.active_button = "Profile Based Job Search"

            data_file = get_files_in_directory(directory='DataFile')[0]
            desired_job_role = None

            with open(data_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith('Desired Job Role:'):
                        desired_job_role = line.split('Desired Job Role:')[1].strip()

            params = {
                        "engine": "google_jobs",
                        "q": desired_job_role,
                        "hl": "en",
                        "ltype": "1",
                        "api_key": SERP_API_KEY
                        }
                        
            if st.session_state.active_button == "Resume Based Job Search":
                # if st.button('Search Job'):
                    with st.spinner('Seaching prefered jobs.....'):
                        resume_pdf_content = ""
                        file_name = get_file_name(directory="ResumeData")
                        file_path = os.path.join("ResumeData", file_name)

                        with open(file_path, 'rb') as file:
                            pdf_reader = PyPDF2.PdfReader(file)
                            for page in range(len(pdf_reader.pages)):
                                resume_pdf_content += pdf_reader.pages[page].extract_text()

                        search = GoogleSearch(params)
                        serp_results = search.get_dict()

                        resume_summary = data_summarizer(llm_api_key=OPENAI_API_KEY, 
                                                        data=resume_pdf_content)
                        
                        if resume_summary and serp_results:
                            job_output_json = job_search_agent(APIKey=OPENAI_API_KEY, 
                                                            LyzrKey=LYZR_X_KEY,
                                                            searchJobData=serp_results,
                                                            candiateSummary=resume_summary)

                            if job_output_json:
                                job_output_json_obj = json.loads(str(job_output_json))
    
                                st.title("Job Listings")

                                for job in job_output_json_obj["matching_jobs"]:
                                    st.subheader(job["title"])
                                    st.write(f"**Company:** {job['company_name']}")
                                    st.write(f"**Description:** {job['description']}")
                                    st.write(f"**Qualifications:** {job['qualifications']}")
                                    st.subheader(f"[Apply Here]({job['apply_link']})")
                                    st.markdown("---")

                                
            elif st.session_state.active_button == "Profile Based Job Search":
                # if st.button('Search Job'):
                    with st.spinner('Seaching prefered jobs.....'):                        
                        with open(data_file, 'r') as file:
                            user_data = file.read()

                        user_profile_summary = data_summarizer(llm_api_key=OPENAI_API_KEY, 
                                                            data=user_data)
                        
                        search = GoogleSearch(params)
                        serp_results = search.get_dict()

                        if user_profile_summary and serp_results:
                            job_output_json = job_search_agent(APIKey=OPENAI_API_KEY, 
                                                            LyzrKey=LYZR_X_KEY,
                                                            searchJobData=serp_results,
                                                            candiateSummary=user_profile_summary)
                            
                            if job_output_json:
                                job_output_json_obj = json.loads(str(job_output_json))
    
                                st.title("Job Listings")

                                for job in job_output_json_obj["matching_jobs"]:
                                    st.subheader(job["title"])
                                    st.write(f"**Company:** {job['company_name']}")
                                    st.write(f"**Description:** {job['description']}")
                                    st.write(f"**Qualifications:** {job['qualifications']}")
                                    st.subheader(f"[Apply Here]({job['apply_link']})")
                                    st.markdown("---")
                    

        except Exception as e:
            st.error(str(e))
    else:
        st.error('Please provide user details on Home page')
       

                                
