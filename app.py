from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_respone(input,pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0], prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file:
        image = pdf2image.convert_from_bytes(upload_file.read(),poppler_path=r'C:\Program Files\poppler-24.07.0\Library\bin')
        first_page = image[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode() #encode to base

        }]  
        return pdf_parts
    else:
        raise FileNotFoundError("File not uploaded")
    

#Streamlit app

st.set_page_config(page_title = "ATS_resume_expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ",key ="input")
upload_file = st.file_uploader("Upload your resume [PDF]...",type = ['pdf'])

if upload_file:
    st.write("pdf was uploaded successfully")

submit1 = st.button("Tell me about the resume")
# submit2 = st.button("How can i improvise my skills?")
submit3 = st.button("Percent Match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


if submit1:
    if upload_file:
        pdf_content = input_pdf_setup(upload_file)
        response = get_gemini_respone(input_prompt1, pdf_content, input_text)
        st.subheader("The response is ")
        st.write(response)
    else:
        st.write('Please upload your resume')

elif submit3:
    if upload_file:
            pdf_content = input_pdf_setup(upload_file)
            response = get_gemini_respone(input_prompt2, pdf_content, input_text)
            st.subheader("The response is ")
            st.write(response)
    else:
        st.write('Please upload your resume')





