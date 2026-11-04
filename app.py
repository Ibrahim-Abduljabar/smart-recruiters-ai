import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import pypdf
import time
from logsnag import LogSnag 
log_client = LogSnag(token=st.secrets["LOGSNAG_TOKEN"]
 log_client.track(channel="visits", event="New Visit")         
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

if st.button(
    f"🚀 ابدأ الفرز والتحليل الذكي للوظيفة رقم {index + 1}",
    key=f"btn_{job['id']}"
):

    if uploaded_files and job_description:

        st.write("## 📊 نتائج الفرز والتحليل الذكي")
        st.success("✅ تم بدء عملية التحليل")

        with st.spinner("⏳ جاري استخراج البيانات وتحليل السير الذاتية..."):

            extracted_data = read_pdfs(uploaded_files)

            for cv in extracted_data:

                with st.container():

                    st.info(f"📁 اسم الملف: {cv['file_name']}")

                    cv_content = cv["content"][:15000]

                    prompt = f"""
                    أنت خبير توظيف وموارد بشرية محترف.

                    قم بتحليل السيرة الذاتية بناءً على الوصف الوظيفي التالي.

                    الوصف الوظيفي:
                    {job_description}

                    --------------------

                    السيرة الذاتية:
                    {cv_content}

                    --------------------

                    المطلوب:

                    1- الاسم الكامل.
                    2- البريد الإلكتروني.
                    3- رقم الهاتف.
                    4- نسبة المطابقة للوظيفة (%).
                    5- أهم 3 نقاط قوة.
                    6- أهم 3 نقاط ضعف.
                    7- المهارات المطابقة للوصف الوظيفي.
                    8- المهارات المفقودة.
                    9- سنوات الخبرة المتوقعة.
                    10- القرار النهائي:
                    - مؤهل للمقابلة
                    - يحتاج مراجعة
                    - غير مؤهل

                    اكتب التقرير باللغة العربية بشكل احترافي ومنظم.
                    """

                    try:

                        completion = client.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        )

                        result = completion.choices[0].message.content

                        st.markdown(result)

                        st.divider()

                        time.sleep(1)

                    except Exception as e:

                        st.error(
                            f"❌ حدث خطأ أثناء تحليل الملف {cv['file_name']}"
                        )

                        st.exception(e)

    else:

        st.error(
            "⚠️ يرجى كتابة الوصف الوظيفي ورفع السير الذاتية أولاً."
        )
