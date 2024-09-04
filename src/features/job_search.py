import streamlit as st
import os
import PyPDF2
from serpapi import GoogleSearch
from utils import (file_checker,
                   save_uploaded_file,
                   get_file_name)

def job_search_assistance(OPENAI_API_KEY, LYZR_X_KEY, SERP_API_KEY):
    st.title('Job Search Assistance')
    st.markdown("##### Find the best fit job for you")

    resume_file = file_checker(directoryName="ResumeData")
    if len(resume_file)>0:

        job_title = st.text_input(label='Provide the prefered job title')
        resume_file_upload = st.file_uploader(label="Upload your resume pdf", type=["pdf"])

        if resume_file_upload and job_title:
            save_uploaded_file(directory="ResumeData", uploaded_file=resume_file_upload)
            if st.button('Search Job'):
                with st.spinner('Seaching prefered job.....'):
                    resume_pdf_content = ""
                    file_name = get_file_name(directory="ResumeData")
                    file_path = os.path.join("ResumeData", file_name)

                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        for page in range(len(pdf_reader.pages)):
                            resume_pdf_content += pdf_reader.pages[page].extract_text()

                    params = {
                            "engine": "google_jobs",
                            "q": f"{job_title}",
                            "hl": "en",
                            "api_key": SERP_API_KEY
                            }

                    search = GoogleSearch(params)
                    results = search.get_dict()
                    jobs_results = results["jobs_results"]

                    for job in jobs_results:
                        st.header(job["title"])
                        st.subheader(f"{job['company_name']} - {job['location']}")
                        
                        st.markdown("### Job Description")
                        st.write(job["description"])
                        
                        for highlight in job["job_highlights"]:
                            st.markdown(f"### {highlight['title']}")
                            for item in highlight["items"]:
                                st.write(f"- {item}")
                        
                        st.markdown("### Apply Links")
                        for apply_option in job["apply_options"]:
                            st.write(f"[{apply_option['title']}]({apply_option['link']})")
                        
                        st.markdown("---")

    else:
        st.error('Please provide user details on Home page')
       

                                
