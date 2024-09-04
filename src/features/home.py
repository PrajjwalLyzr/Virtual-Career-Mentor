import streamlit as st
import os
from PIL import Image
from utils import (remove_existing_files,
                   save_uploaded_file,
                   delete_data_file)


def home_page_feature():
    resume_file_dir = "ResumeData"
    os.makedirs(resume_file_dir, exist_ok=True)
    remove_existing_files(directory=resume_file_dir)

    # data_file_path = "data_file.txt"
    # delete_data_file(file_path=data_file_path)

    data_file_dir = 'DataFile'
    os.makedirs(data_file_dir, exist_ok=True)
    remove_existing_files(directory=data_file_dir)

    image = Image.open("./src/logo/lyzr-logo.png")
    st.image(image, width=150)

    st.title('Virtual Carrer Mentor')
    st.markdown("##### Provide your details")
    
    col1, col2 = st.columns(2)

    with col1:
        user_name = st.text_input(label="Enter your name")
        user_location = st.text_input(label="Enter the location")
        career_goals = st.text_area(label="Enter your Carrer Goals", 
                                    placeholder="Career goals (e.g., industry switch, promotion)", 
                                    height=100)

    with col2:
        user_education = st.text_input(label="Enter your Education")
        user_current_job = st.text_input(label="Enter your current job title")
        skills_experience = st.text_area(label="Write about your skills/experiemce", 
                                         placeholder="Skills and experience (input as bullet points or text)", 
                                         height=100)

    desired_job_role = st.text_input(label='Desired Job Role')

    resume_file = st.file_uploader("Upload your resume pdf file", type=["pdf"])

    if (user_name and user_location and career_goals and 
        user_education and user_current_job and skills_experience and 
        desired_job_role and resume_file) is not None:

        col3, col4 = st.columns(2)

        with col3:
            if st.button('Submit'):
                save_uploaded_file(directory=resume_file_dir, uploaded_file=resume_file)
                with open(f'{data_file_dir}/data_file.txt', 'w') as file:
                    file.write(f"Name: {user_name}\n")
                    file.write(f"Location: {user_location}\n")
                    file.write(f"Career Goals: {career_goals}\n")
                    file.write(f"Education: {user_education}\n")
                    file.write(f"Current Job Title: {user_current_job}\n")
                    file.write(f"Skills/Experience: {skills_experience}\n")
                    file.write(f"Desired Job Role: {desired_job_role}\n")

                    st.success('Details has been submited')
        
        with col4:
            if st.button('Delete'):
                remove_existing_files(directory='DataFile')
                remove_existing_files(directory='ResumeData')
                st.error('Data got Deleted')