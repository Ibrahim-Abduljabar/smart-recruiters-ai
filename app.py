import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import pypdf
import time
from logsnag import LogSnag 
log_client = LogSnag(token=st.secrets["LOGSNAG_TOKEN"], project="smart-recruiters")

log_client.track(channel="visits", event="New Visit")

st.set_page_config(
    page_title="SmartRecruiters AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.write("### SmartRecruiters AI 📑🚀")
st.caption(" An intelligent CV screening and filtering system powered by advanced AI algorithms.")
st.divider()

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

def read_pdfs(uploaded_files):
    cvs_test_list = []
    for file in uploaded_files:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += str(page.extract_text() or "")
        cvs_test_list.append({"file_name": file.name, "content": text})
    return cvs_test_list

if "jobs_list" not in st.session_state:
    st.session_state.jobs_list = [{"id": 0}]

st.write("#### 🛠️ Sorting and Input Settings")

for index, job in enumerate(st.session_state.jobs_list):
    st.write(f"##### 📌Recruitment Campaign No. ({index + 1})")
    
    job_description = st.text_area(
        f"Enter the required job description for job number{index + 1}:", 
        height=150, 
        key=f"desc_{job['id']}"
    )
    uploaded_files = st.file_uploader(
        f"Upload the CVs of candidates for job number{index + 1}:", 
        type=["pdf"], 
        accept_multiple_files=True, 
        key=f"files_{job['id']}"
    )
    
    if st.button(f"🚀Start sorting and intelligent analysis for job number {index + 1}", key=f"btn_{job['id']}"):
        if uploaded_files and job_description:
            st.write("#### 📊 Processing data and presenting results in professional cards.")
            st.write("🔍 Performing analysis and smart matching...")
            
            with st.spinner("⏳ Data extraction and advanced AI-powered sorting in progress..."):
                extracted_data = read_pdfs(uploaded_files)
                
                for cv in extracted_data:
                    with st.container():
                        st.info(f"📁 Candidate Profile: {cv['file_name']}")
                        
                        prompt = f"""
                        Analyze the resume based on the specified job description.
                        
                        Job Description:
                        {job_description}
                        
                        the biography:
                        {cv['content']}
                        
                        ---
                        Accurately extract the following information in Arabic:
                        1. Name, email, and phone number (if available).
                        2. Candidate-to-job match percentage (state a clear percentage, e.g., 85%).
                        3. Strengths and weaknesses (very briefly).
                        4. Final decision (qualified for interview / not qualified).
                        """
                        
                        completion = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        
                        st.markdown(completion.choices[0].message.content)
                        st.write("---")
                        time.sleep(1)
        else:
            st.error("⚠️ Please make sure to write the job description and upload the CVs first!")
    
    st.write("---")

if st.button("➕ Adding a section for another job"):
    new_id = len(st.session_state.jobs_list)
    st.session_state.jobs_list.append({"id": new_id})
    st.rerun()

    
