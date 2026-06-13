import streamlit as st
from groq import Groq
import pypdf
import time

# 1. ضبط إعدادات الصفحة الاحترافية وتفعيل وضع التمركز التلقائي للمظهر المظلم
st.set_page_config(
    page_title="SmartRecruiters AI", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. ترويسة الموقع بشكل منسق ومحترم للعين
st.write("### SmartRecruiters AI 🚀")
st.caption("نظام الفرز والتصفية الذكي للسير الذاتية بالاعتماد على خوارزميات الذكاء الاصطناعي الفائقة")
st.divider()

# 3. جلب مفتاح الـ API والاتصال بـ Groq
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# دالة قراءة ملفات الـ PDF
def read_pdfs(uploaded_files):
    cvs_test_list = []
    for file in uploaded_files:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += str(page.extract_text() or "")
        cvs_test_list.append({"file_name": file.name, "content": text})
    return cvs_test_list

# 4. تنظيم منطقة المدخلات داخل حاوية أنيقة
with st.container():
    st.write("#### 📥 إعدادات الفرز والمدخلات")
    job_description = st.text_area("أدخل الوصف الوظيفي المطلوب (Job Description):", height=150, placeholder="انسخ متمتطلبات الوظيفة هنا...")
    uploaded_files = st.file_uploader("ارفع السير الذاتية للمرشحين (PDF)", type=["pdf"], accept_multiple_files=True)

st.divider()

# 5. معالجة البيانات وعرض النتائج بشكل "بطاقات احترافية"
if uploaded_files and job_description:
    st.write("#### 📊 نتائج التحليل والمطابقة الذكية")
    
    # استخدام شريط تحميل احترافي يوضح أن النظام يقوم بعمليات معقدة
    with st.spinner("⏳ جاري استخراج البيانات والفرز المتقدم بالذكاء الاصطناعي..."):
        extracted_data = read_pdfs(uploaded_files)
        
        for cv in extracted_data:
            # وضع كل نتيجة في حاوية منفصلة ومحترمة (Card Style)
            with st.container():
                st.info(f"📄 ملف المرشح: {cv['file_name']}")
                
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
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # تصحيح الـ Bug وعرض المحتوى بشكل سليم داخل الحاوية
                st.markdown(completion.choices[0].message.content)
                st.write("---") # خط فاصل ناعم بين المرشحين

time.sleep(2)
