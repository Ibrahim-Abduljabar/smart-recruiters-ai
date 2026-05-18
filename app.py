import streamlit as st
from groq import Groq
import pypdf

st.set_page_config(page_title="SmartRecruiters AI", layout="centered")
st.title("SmartRecruiters AI 🚀")

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

job_description = st.text_area("أدخل الوصف الوظيفي (Job Description) للمقارنة:")
uploaded_files = st.file_uploader("ارفع السير الذاتية (PDF)", type=["pdf"], accept_multiple_files=True)

if uploaded_files and job_description:
    with st.spinner("جاري التحليل والفرز المتقدم..."):
        extracted_data = read_pdfs(uploaded_files)
        for cv in extracted_data:
            st.subheader(f"📄 نتائج تحليل: {cv['file_name']}")
            
            prompt = f"""
            قم بتحليل السيرة الذاتية بناءً على الوصف الوظيفي المحدد.
            
            الوصف الوظيفي:
            {job_description}
            
            السيرة الذاتية:
            {cv['content']}
            
            استخرج المخرجات التالية بدقة باللغة العربية:
            1. الاسم، البريد الإلكتروني، ورقم الهاتف (إن وجد).
            2. نسبة مطابقة المرشح للوظيفة (اكتب نسبة مئوية واضحة مثل 85%).
            3. نقاط القوة ونقاط الضعف باختصار شديد.
            4. القرار النهائي (مؤهل للمقابلة / غير مؤهل).
            """
            completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
            st.success("تم التقييم بنجاح!")
            st.markdown(completion.choices[0].message.content)
            st.divider()
