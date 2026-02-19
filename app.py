import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(
    page_title="قصتي",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS للتصميم الجميل
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 قصتي")
st.subheader("تطبيق توليد قصص أطفال")

# نموذج الإدخال
with st.form("story_form"):
    child_name = st.text_input("اسم الطفل", placeholder="مثال: أحمد")
    
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "اللغة",
            ["AR", "FR", "EN"],
            format_func=lambda x: {"AR": "🇩🇿 العربية", "FR": "🇫🇷 Français", "EN": "🇬🇧 English"}[x]
        )
    with col2:
        story = st.selectbox(
            "القصة",
            ["time_machine", "space", "pirate"],
            format_func=lambda x: {
                "time_machine": "⏰ رحلة عبر الزمن",
                "space": "🚀 رحلة الفضاء",
                "pirate": "🏴‍☠️ مغامرة القراصنة"
            }[x]
        )
    
    uploaded_file = st.file_uploader(
        "📷 صورة الطفل",
        type=["jpg", "jpeg", "png"],
        help="اختر صورة واضحة للوجه"
    )
    
    submitted = st.form_submit_button("✨ إنشاء القصة")

# معالجة الطلب
if submitted:
    if not child_name or not uploaded_file:
        st.error("❌ الرجاء إدخال الاسم واختيار صورة")
    else:
        with st.spinner("🎨 جاري إنشاء القصة... قد يستغرق 30-60 ثانية"):
            try:
                # تحويل الصورة
                image = Image.open(uploaded_file)
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # إرسال لـ RunPod
                response = requests.post(
                    "https://api.runpod.ai/v2/rlydf3a15qv86b/run",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer rpa_YUF652M25EB1I1IQAWDT988YIXQYLZKNN945AT9Eudu63j"
                    },
                    json={
                        "input": {
                            "prompt": f"Children's book illustration of {child_name} in {story} story, Pixar style, storybook art, magical atmosphere",
                            "image": f"data:image/png;base64,{img_base64}",
                            "width": 1024,
                            "height": 1024,
                            "steps": 30
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    job_id = data.get('id', 'N/A')
                    
                    st.success(f"✅ تم إرسال الطلب بنجاح!")
                    st.info(f"🆔 رقم الطلب: `{job_id}`")
                    st.warning("⏳ الصورة قيد المعالجة في RunPod...")
                    
                    # رابط التحقق من الحالة
                    check_url = f"https://api.runpod.ai/v2/r1ydf3al5qv86b/status/{job_id}"
                    st.code(check_url, language="bash")
                    
                else:
                    st.error(f"❌ خطأ من RunPod: {response.status_code}")
                    st.text(response.text)
                    
            except requests.exceptions.Timeout:
                st.error("⏰ انتهى الوقت - حاول مرة أخرى")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# تذييل
st.markdown("---")
st.caption("صنع ب❤️ لأطفالنا")
