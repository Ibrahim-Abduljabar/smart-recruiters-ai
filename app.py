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

st.markdown("""
    <style>
        /* خلفية الصفحة */
        .stApp {
            background-color: #0d0d0d !important;
        }

        /* النص */
        body, p, span, label {
            color: #f2f2f2 !important;
        }

        /* العناوين */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }

        /* الأزرار */
        button[kind="primary"] {
            background-color: #4a4a4a !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }

        /* مربعات الإدخال */
        textarea, input {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
        }

        /* الـ sidebar */
        .css-1d391kg, .css-1cypcdb {
            background-color: #111111 !important;
        }

        /* فواصل */
        hr {
            border: 1px solid #333 !important;
        }

        /* بطاقات المعلومات */
        .stAlert {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

st.write("### SmartRecruiters AI 📑🚀")
st.caption(" نظام الفرز والتصفية الذكي للسير الذاتية بالاعتماد على خوارزميات الذكاء الاصطناعي الفائقة")
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

st.write("#### 🛠️ إعدادات الفرز والمدخلات")

for index, job in enumerate(st.session_state.jobs_list):
    st.write(f"##### 📌 الحملة التوظيفية رقم ({index + 1})")
    
    job_description = st.text_area(
        f"أدخل الوصف الوظيفي المطلوب للوظيفة رقم {index + 1}:", 
        height=150, 
        key=f"desc_{job['id']}"
    )
    uploaded_files = st.file_uploader(
        f"ارفع السير الذاتية للمرشحين للوظيفة رقم {index + 1}:", 
        type=["pdf"], 
        accept_multiple_files=True, 
        key=f"files_{job['id']}"
    )
    
    if st.button(f"🚀 ابدأ الفرز والتحليل الذكي للوظيفة رقم {index + 1}", key=f"btn_{job['id']}"):
        if uploaded_files and job_description:
            st.write("#### 📊 معالجة البيانات وعرض النتائج بشكل بطاقات احترافية")
            st.write("🔍 جاري التحليل والمطابقة الذكية...")
            
            with st.spinner("⏳ جاري استخراج البيانات والفرز المتقدم بالذكاء الاصطناعي..."):
                extracted_data = read_pdfs(uploaded_files)
                
                for cv in extracted_data:
                    with st.container():
                        st.info(f"📁 ملف المرشح: {cv['file_name']}")
                        
                        prompt = f"""
                        قم بتحليل السيرة الذاتية بناءً على الوصف الوظيفي المحدد.
                        
                        الوصف الوظيفي:
                        {job_description}
                        
                        السيرة الذاتية:
                        {cv['content']}
                        
                        ---
                        استخرج المخرجات التالية بدقة باللغة العربية:
                        1. الاسم والبريد الإلكتروني ورقم الهاتف (إن وجد).
                        2. نسبة مطابقة المرشح للوظيفة (اكتب نسبة مئوية واضحة مثل 85%).
                        3. نقاط القوة ونقاط الضعف باختصار شديد.
                        4. القرار النهائي (مؤهل للمقابلة / غير مؤهل).
                        """
                        
                        completion = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        
                        st.markdown(completion.choices[0].message.content)
                        st.write("---")
                        time.sleep(1)
        else:
            st.error("⚠️ من فضلك تأكد من كتابة الوصف الوظيفي ورفع السير الذاتية أولاً!")
    
    st.write("---")

if st.button("➕ إضافة قسم لوظيفة أخرى"):
    new_id = len(st.session_state.jobs_list)
    st.session_state.jobs_list.append({"id": new_id})
    st.rerun()
