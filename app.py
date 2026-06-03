import streamlit as st
import time
import pandas as pd

# 1. إعدادات الصفحة والـ Session State الأساسية
st.set_page_config(page_title="ReliefGrid Crisis Platform", page_icon="🌐", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = 1  # نبدأ دايماً بالشاشة الأولى
if "queue" not in st.session_state:
    st.session_state.queue = []  # طابور الانتظار المحلي

# دالة مخصصة لعمل فريم الموبايل وضبط الأزرار
st.markdown("""
    <style>
    .block-container { max-width: 450px; padding-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .status-box { padding: 8px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 14px; }
    .lang-bar { font-size: 14px; padding-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. الهيدر الثابت (الشبكة واللغات)
col1, col2 = st.columns([2, 1.5])
with col1:
    st.markdown('<div class="lang-bar">🌐 <b>العربية</b> | English</div>', unsafe_allow_html=True)

with col2:
    network_status = st.toggle("Network", value=True, label_visibility="collapsed")
    if network_status:
        st.markdown('<div class="status-box" style="background-color: #d4edda; color: #155724;">🟢 Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-box" style="background-color: #f8d7da; color: #721c24;">🔴 Offline</div>', unsafe_allow_html=True)

st.write("---")

# ==========================================
# 📱 الشاشة 1: Emergency Reporting (الأوفلاين أولاً)
# ==========================================
if st.session_state.page == 1:
    st.markdown("<h3 style='text-align: center;'>📱 الشاشة 1: البلاغ العاجل</h3>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📸 التقاط أو رفع صورة الأضرار للمبنى", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="تم تحميل الصورة بنجاح", use_container_width=True)
        
    description = st.text_area("📝 وصف الأضرار الهيكلية أو الحالة العاجلة", placeholder="اكتب تفاصيل البلاغ هنا...")
    
    if st.button("التالي: تقييم الخدمات ➡️"):
        if not description:
            st.error("⚠️ من فضلك اكتب وصفاً للبلاغ أولاً!")
        else:
            st.session_state.temp_report = {"description": description} # حفظ مؤقت
            st.session_state.page = 2
            st.rerun()

# ==========================================
# 📱 الشاشة 2: Initial Structural & Utility Assessment
# ==========================================
elif st.session_state.page == 2:
    st.markdown("<h3 style='text-align: center;'>⚡ الشاشة 2: تقييم الخدمات</h3>", unsafe_allow_html=True)
    
    st.write("#### شبكة الكهرباء (Electricity Grid)")
    electricity = st.radio("مدى الضرر بالكهرباء:", ["لا يوجد ضرر (No Damage)", "ضرر جزئي (Partial)", "انقطاع كامل (Total)"])
    
    st.write("#### شبكة المياه (Water Grid)")
    water = st.radio("حالة المياه:", ["تعمل (Working)", "منقطعة (Interrupted)"])
    
    st.write("#### الاحتياجات العاجلة (Immediate Human Needs)")
    needs = st.multiselect("اختر الاحتياجات المطلوبة:", ["مأوى (Shelter)", "طعام ومياه (Food & Water)", "رعاية طبية (Medical)"])
    
    col_b, col_n = st.columns(2)
    with col_b:
        if st.button("⬅️ رجوع"):
            st.session_state.page = 1
            st.rerun()
    with col_n:
        if st.button("التالي: تحديد الموقع ➡️"):
            st.session_state.temp_report.update({
                "electricity": electricity,
                "water": water,
                "needs": needs
            })
            st.session_state.page = 3
            st.rerun()

# ==========================================
# 📱 الشاشة 3: Offline MapGrid & Caching Queue
# ==========================================
elif st.session_state.page == 3:
    st.markdown("<h3 style='text-align: center;'>🗺️ الشاشة 3: خريطة الـ MapGrid والأوفلاين</h3>", unsafe_allow_html=True)
    
    st.info("🛰️ نظام MapGrid: تم تحميل شبكة الإحداثيات المحلية الخفيفة مسبقاً لتعمل بدون إنترنت.")
    
    # محاكاة إحداثيات ثابتة زي الفيجما بالظبط
    st.success("📍 الإحداثيات الملتقطة عبر الـ GPS: Lat: 30.044 / Lon: 31.235")
    
    col_b, col_s = st.columns(2)
    with col_b:
        if st.button("⬅️ رجوع"):
            st.session_state.page = 2
            st.rerun()
            
    with col_s:
        if st.button("🚀 إرسال البلاغ النهائي"):
            with st.spinner("جاري تشفير وضغط البيانات كـ Protocol Buffer..."):
                time.sleep(1)
                
                final_report = st.session_state.temp_report
                final_report["lat"] = 30.044
                final_report["lon"] = 31.235
                
                if network_status:
                    # لو أونلاين يروح عل طول للـ Dashboard
                    st.session_state.queue.append(final_report)
                    st.success("✅ تم الإرسال الفوري للوحة تحكم UNDP!")
                else:
                    # لو أوفلاين يتخزن في الـ Queue
                    st.session_state.queue.append(final_report)
                    st.warning("📥 لا يوجد إنترنت! تم الحفظ في الـ Local Queue بنجاح.")
                
                time.sleep(1.5)
                st.session_state.page = 4
                st.rerun()

# ==========================================
# 📊 الشاشة 4: UNDP Crisis Bureau Dashboard (The Sync)
# ==========================================
elif st.session_state.page == 4:
    st.markdown("<h2 style='text-align: center; color: #1a73e8;'>📊 UNDP Crisis Bureau Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>لوحة التحكم المركزية واستقبال البيانات المجمعة</p>", unsafe_allow_html=True)
    
    # زرار للتحميل بصيغة CSV/JSON زي ما رسمتي فوق
    st.button("📦 Exported Structured Data: CSV / JSON")
    
    # إحصائيات محاكاة ذكية بناءً على الداتا اللي دخلت
    st.write("### 📈 التحليلات والرسوم البيانية الرسمية")
    
    # داتا افتراضية مضاف إليها البلاغات الجديدة جوه الـ Queue
    total_cases = 500 + len(st.session_state.queue)
    urgent_needs = 180 + (len(st.session_state.queue) * 2)
    
    # رسم الـ Bar Chart بنفس أرقام الفيجما بتاعتكِ!
    chart_data = pd.DataFrame(
        [total_cases, urgent_needs],
        index=["الحالات الحرجة", "الاحتياجات العاجلة"],
        columns=["العدد"]
    )
    st.bar_chart(chart_data)
    
    st.write("---")
    if st.button("🔄 تقديم بلاغ جديد (العودة للشاشة 1)"):
        st.session_state.page = 1
        st.rerun()
        