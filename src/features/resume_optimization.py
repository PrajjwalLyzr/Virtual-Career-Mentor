import streamlit as st
import os
import time
import PyPDF2
from agents import resume_optimization_agent
from utils import (file_checker,
                   get_file_name,
                   get_files_in_directory)


def resume_optimization_feature(OPENAI_API_KEY, LYZR_X_KEY):
    st.title('Resume Optimization')
    st.markdown("##### Optimize your resume")

    data_file = file_checker(directoryName="DataFile")
    if len(data_file)>0:
        if st.button('Optimize Resume'):
            with st.spinner('Optimizing the Resume'):            
                resume_pdf_content = ""
                file_name = get_file_name(directory="ResumeData")
                file_path = os.path.join("ResumeData", file_name)

                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in range(len(pdf_reader.pages)):
                        resume_pdf_content += pdf_reader.pages[page].extract_text()

                desired_job_role = None
                career_goal = None
                skills_experience = None
                data_file = get_files_in_directory(directory='DataFile')[0]

                try:
                    with open(data_file, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            if line.startswith('Desired Job Role:'):
                                desired_job_role = line.split('Desired Job Role:')[1].strip()
                            elif line.startswith('Career Goals:'):
                                career_goal = line.split('Career Goals:')[1].strip()
                            elif line.startswith('Skills/Experience:'):
                                skills_experience = line.split('Skills/Experience:')[1].strip()

                    resume_suggestions = resume_optimization_agent(APIKey=OPENAI_API_KEY, 
                                                                LyzrKey=LYZR_X_KEY, 
                                                                resumeData=resume_pdf_content,
                                                                desiredJob=desired_job_role,
                                                                careerGoal=career_goal,
                                                                skillsExperience=skills_experience)

                    st.write(resume_suggestions)
                    
                except Exception as e:
                    st.error(str(e))

    else:
        st.error('Please provide user details on Home page')

    