import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="ML Performance Intelligence System",
    page_icon="🧠",
    layout="centered"
)

# ---------------- THEME ----------------
theme = st.sidebar.radio("🎨 Theme", ["🌞 Light", "🌙 Dark"])

if theme == "🌙 Dark":
    bg = "#0e1117"
    card = "#1a1f2b"
    text = "#ffffff"
    border = "#2a3142"
else:
    bg = "#ffffff"
    card = "#f5f7fb"
    text = "#111111"
    border = "#e5e7eb"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text};
}}

h1, h2, h3, p {{
    color: {text} !important;
}}

div[data-testid="stMetric"] {{
    background-color: {card};
    border: 1px solid {border};
    padding: 15px;
    border-radius: 12px;
}}

.stButton>button {{
    background-color: #6C63FF;
    color: white;
    border-radius: 10px;
    padding: 10px;
}}

.block {{
    background-color: {card};
    padding: 18px;
    border-radius: 15px;
    border: 1px solid {border};
    margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🧠 ML Performance Intelligence System")

# ---------------- MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- INPUT ----------------
st.sidebar.header("🎯 Enter Your Stats")

target = st.sidebar.slider("🎯 Target Score", 40, 100, 85)
study_hours = st.sidebar.slider("📚 Study Hours", 0.0, 10.0, 5.0)
sleep_hours = st.sidebar.slider("😴 Sleep Hours", 4.0, 10.0, 7.0)
attendance = st.sidebar.slider("🏫 Attendance %", 50, 100, 80)
social_media = st.sidebar.slider("📱 Social Media Hours", 0.0, 8.0, 2.0)
stress = st.sidebar.slider("😰 Stress Level", 1, 10, 5)

# ---------------- ANALYZE ----------------
if st.button("🚀 Analyze My Performance"):

    input_data = np.array([[study_hours, sleep_hours, social_media, stress, attendance]])
    predicted_score = model.predict(input_data)[0]
    gap = target - predicted_score

    # ---------------- RESULT ----------------
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("📊 Prediction Result")

    st.metric("Predicted Score", f"{predicted_score:.2f}%")
    st.progress(min(int(predicted_score), 100) / 100)

    if predicted_score >= target:
        st.success("✅ You are on track to achieve your target!")
    else:
        st.error(f"⚠️ You are short by {gap:.2f}%")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- INSIGHTS (RESTORED FULL SECTION) ----------------
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("🧠 What You're Doing Right & What to Improve")

    strengths = []
    weaknesses = []

    if study_hours >= 6:
        strengths.append("Strong study routine")
    else:
        weaknesses.append("Increase study hours")

    if attendance >= 85:
        strengths.append("Good attendance")
    else:
        weaknesses.append("Improve attendance")

    if 7 <= sleep_hours <= 8:
        strengths.append("Healthy sleep cycle")
    else:
        weaknesses.append("Fix sleep schedule")

    if social_media <= 3:
        strengths.append("Good digital discipline")
    else:
        weaknesses.append("Reduce social media usage")

    if stress <= 5:
        strengths.append("Stress under control")
    else:
        weaknesses.append("Manage stress better")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ What You're Doing Right")
        for s in strengths:
            st.success(s)

    with col2:
        st.subheader("❌ What to Improve")
        for w in weaknesses:
            st.warning(w)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- FEATURE CONTRIBUTION GRAPH ----------------
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("📊 What is affecting your score?")

    features = ["Study", "Sleep", "Social Media", "Stress", "Attendance"]

    contributions = [
        study_hours * 6,
        sleep_hours * 4,
        -social_media * 5,
        -stress * 4,
        attendance * 0.3
    ]

    fig, ax = plt.subplots()
    colors = ['green' if c > 0 else 'red' for c in contributions]

    ax.bar(features, contributions, color=colors)
    ax.set_ylabel("Impact on Score")
    ax.set_title("Feature Contribution")
    ax.axhline(0, color='black')

    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- WHAT IF SIMULATOR ----------------
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("🔮 What-If Improvement Simulator")

    improved_input = np.array([[
        min(study_hours + 1, 10),
        min(sleep_hours + 1, 10),
        max(social_media - 1, 0),
        max(stress - 1, 1),
        min(attendance + 5, 100)
    ]])

    improved_score = model.predict(improved_input)[0]
    gain = improved_score - predicted_score

    st.info(f"If you improve habits slightly, your score could increase by **{gain:.2f}%**")
    st.progress(min(int(improved_score), 100))

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- FINAL MESSAGE ----------------
    if predicted_score >= 90:
        st.success("🔥 Excellent performance profile")
    elif predicted_score >= 75:
        st.info("👍 Good profile — small improvements needed")
    else:
        st.error("⚠️ Needs consistent improvement")
