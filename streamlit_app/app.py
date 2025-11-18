# import streamlit as st
# from streamlit_lottie import st_lottie
# import json
# from predictor import predict_career
# from resume_parser import extract_skills_from_pdf
# from personality_quiz import get_quiz_questions, evaluate_personality, generate_technical_questions
# import base64
# from io import BytesIO
# from fpdf import FPDF
# from datetime import datetime

# # === Load Skills Gap Module ===
# from skills_gap import get_missing_skills  # 🔥 NEW

# # === For chatbot conversation import ===
# from chatbot import careerbot_chat 
# import os
# import urllib.request

# # === 🔥 Download DejaVu Font if not present ===
# def get_dejavu_font_path():
#     return "fonts/DejaVuSans.ttf"

# st.set_page_config(page_title="AI Career Counselor", page_icon="🎓", layout="wide")

# # Load animations
# @st.cache_data(show_spinner=False)
# def load_lottie(path: str):
#     with open(path, "r") as f:
#         return json.load(f)

# career_animation = load_lottie("streamlit_app/assets/career.json")
# quiz_animation = load_lottie("streamlit_app/assets/quiz.json")
# resume_animation = load_lottie("streamlit_app/assets/resume.json")

# # Theme toggle
# if 'dark_mode' not in st.session_state:
#     st.session_state.dark_mode = False

# st.session_state.dark_mode = st.toggle("🌗 Toggle Dark Mode", value=st.session_state.dark_mode)

# if st.session_state.dark_mode:
#     st.markdown("""
#         <style>
#             body { background-color: #0e1117; color: white; }
#             .stButton>button { background-color: #1f77b4; color: white; transition: background-color 0.3s ease; }
#             .stButton>button:hover { background-color: #145a86; }
#         </style>
#     """, unsafe_allow_html=True)
# else:
#     st.markdown("""
#         <style>
#             .stButton>button { background-color: #f0f2f6; color: black; transition: background-color 0.3s ease; }
#             .stButton>button:hover { background-color: #d6dce5; }
#         </style>
#     """, unsafe_allow_html=True)

# st.title("🎓 AI Career Counselor")
# st.markdown("""
# Welcome to your smart career guide! This tool analyzes your resume and personality to recommend suitable tech careers.
# """)

# # === PDF Report Generator ===
# def create_pdf(skills, recommendations, missing_skills_by_career=None):
#     from fpdf import FPDF
#     from datetime import datetime
#     from io import BytesIO
#     import re

#     def sanitize_text(text):
#         text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
#         text = ''.join(ch if ch.isprintable() else ' ' for ch in text)
#         return text.strip()

#     def split_long_words(text, max_length=40):
#         words = text.split()
#         new_words = []
#         for w in words:
#             if len(w) > max_length:
#                 parts = [w[i:i+max_length] for i in range(0, len(w), max_length)]
#                 new_words.extend(parts)
#             else:
#                 new_words.append(w)
#         return ' '.join(new_words)

#     class PDFWithWatermark(FPDF):
#         def header(self):
#             self.image("streamlit_app/assets/logo_watermark.png", x=5, y=20, w=200)

#     pdf = PDFWithWatermark()
#     pdf.set_margins(left=15, top=15, right=15)
#     pdf.add_page()

#     font_path = get_dejavu_font_path()
#     pdf.add_font("DejaVu", "", font_path, uni=True)
#     pdf.set_font("DejaVu", "", 16)
#     pdf.ln(10)
#     pdf.cell(0, 10, "Career Recommendations", ln=True, align="C")
#     pdf.ln(10)

#     pdf.set_font("DejaVu", "", 12)
#     skills_text = ', '.join([sanitize_text(s) for s in skills])
#     skills_text = split_long_words(skills_text)
#     pdf.multi_cell(w=180, h=10, txt=f"Extracted Skills: {skills_text}", new_x="LEFT")
#     pdf.ln(5)

#     pdf.cell(0, 10, "Top Recommended Careers:", ln=True)
#     pdf.ln(5)
#     for career in recommendations:
#         ctext = sanitize_text(career)
#         ctext = split_long_words(ctext)
#         pdf.multi_cell(w=180, h=10, txt=ctext, new_x="LEFT")

#     # Add a new page before missing skills section to prevent overflow
#     if missing_skills_by_career:
#         pdf.add_page()
#         pdf.ln(10)
#         pdf.set_font("DejaVu", "", 14)
#         pdf.cell(0, 10, "Skills You Might Need to Learn:", ln=True)

#         any_missing = False
#         for career in recommendations:
#             required_skills = missing_skills_by_career.get(career, [])

#             if required_skills:
#                 any_missing = True
#                 pdf.ln(5)
#                 pdf.set_font("DejaVu", "", 12)

#                 if pdf.get_y() > 260:
#                     pdf.add_page()

#                 pdf.cell(0, 10, sanitize_text(career), ln=True)

#                 for skill in required_skills:
#                     clean_skill = sanitize_text(skill)
#                     if clean_skill:
#                         clean_skill = split_long_words(clean_skill)

#                         if pdf.get_y() > 260:
#                             pdf.add_page()

#                         try:
#                             pdf.multi_cell(w=180, h=10, txt=f"- {clean_skill}", new_x="LEFT")
#                         except Exception as e:
#                             pdf.cell(0, 10, f"- [Error displaying skill]", ln=True)

#         if not any_missing:
#             pdf.ln(10)
#             pdf.set_font("DejaVu", "", 12)
#             pdf.multi_cell(w=180, h=10, txt="You're all set! No new skills required.", new_x="LEFT")

#     # Footer
#     pdf.set_y(-15)
#     pdf.set_font("DejaVu", "", 10)
#     pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 0, "C")

#     pdf_output = BytesIO()
#     pdf.output(pdf_output)
#     return pdf_output.getvalue()




# # === Step Navigation ===
# step = st.selectbox("Navigate to Step:", ["Introduction", "Resume Upload", "Personality Quiz", "Prediction", "Chat Summary", "Skills Gap Filler"])
# tabs = st.tabs([
#     "🏁 Introduction",
#     "📄 Resume Upload",
#     "🧠 Personality Quiz",
#     "📝 Chat Summary",
#     "ℹ️ About"
# ])


# # === Tab 1: Introduction ===
# with tabs[0]:
#     col1, col2 = st.columns([1, 2])
#     with col1:
#         st_lottie(career_animation, height=300)
#     with col2:
#         st.subheader("What can this app do?")
#         st.markdown("""
#         - Extract your skills from your resume (PDF)
#         - Ask a few smart personality-based questions
#         - Predict the best career paths based on both
#         """)
#         st.success("Get started by uploading your resume or answering a quick quiz!")

# # === Tab 2: Resume Upload ===
# with tabs[1]:
#     st.subheader("📄 Upload Your Resume")
#     col1, col2 = st.columns([2, 1])

#     with col1:
#         uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
#         if uploaded_file is not None:
#             with st.spinner("⏳ Extracting skills and education from your resume..."):
#                 st.session_state.resume_data = extract_skills_from_pdf(uploaded_file)
#                 resume_data = st.session_state.resume_data

#             st.success("✅ Resume processed successfully!")
#             st.markdown(f"**📌 Name:** `{resume_data['name']}`")
#             st.markdown(f"**🎓 Education Level:** `{resume_data['education']}`")
#             st.markdown("**🛠 Skills:**")
#             st.code(", ".join(resume_data["skills"]), language="markdown")

#     with col2:
#         st_lottie(resume_animation, height=300)

# # === Tab 3: Personality Quiz ===
# with tabs[2]:
#     if "resume_data" not in st.session_state:
#         st.warning("Please upload your resume first to extract skills.")
#     else:
#         skills = st.session_state.resume_data.get("skills", [])

#         technical_questions = generate_technical_questions(skills)
#         quiz_questions = get_quiz_questions() + technical_questions

#         st.subheader("Answer the following questions (1 - Strongly Disagree to 5 - Strongly Agree):")
#         responses = []
#         for i, q in enumerate(quiz_questions):
#             score = st.slider(q['question'], 1, 5, 3, key=f"quiz_{i}")
#             responses.append(score)

#     if st.button("Evaluate Personality and Show Careers"):
#         recommendations = evaluate_personality(responses, quiz_questions)
#         st.session_state["quiz_recommendations"] = recommendations  # store for reuse

#         st.success("Top Recommended Careers:")
#         for career in recommendations:
#             st.markdown(f"✅ {career}")

#         career_skill_map = {career: get_missing_skills(skills, career) for career in recommendations}
#         normalized_resume_skills = set(s.lower().strip() for s in skills)
#         st.markdown("### Skills You Might Need to Learn:")
#         for career, missing in career_skill_map.items():
#             filtered_missing = [m for m in missing if m.lower().strip() not in normalized_resume_skills]
#             st.markdown(f"**🔹 {career}:** {', '.join(filtered_missing) if filtered_missing else 'You\'re good!'}")

#         pdf_bytes = create_pdf(skills, recommendations, career_skill_map)
#         st.session_state["pdf_bytes"] = pdf_bytes  # save PDF to session state

#     # Show download button if PDF exists in session state
#     if "pdf_bytes" in st.session_state:
#         st.download_button(
#             label="📄 Download Career Report (PDF)",
#             data=st.session_state["pdf_bytes"],
#             file_name=f"career_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
#             mime="application/pdf"
#         )

# # === Tab 4: Chat Summary ===
# with tabs[3]:
#     st.subheader("🤖 AI Career Counselor Chatbot")

#     # Initialize chat history if not already present
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     # Chat container with fixed height and scroll
#     chat_container_style = """
#         max-height: 400px; 
#         overflow-y: auto; 
#         padding: 10px; 
#         border: 1px solid #ccc; 
#         border-radius: 10px; 
#         background-color: #f5f5f5;
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     """

#     # Display chat messages with user and bot styles
#     def render_message(sender, message):
#         user_style = """
#             background-color: #d1e7dd; 
#             padding: 10px 14px; 
#             border-radius: 15px; 
#             max-width: 70%;
#             margin-bottom: 8px; 
#             align-self: flex-end;
#             font-size: 14px;
#             color: #000;
#         """
#         bot_style = """
#             background-color: #f8d7da; 
#             padding: 10px 14px; 
#             border-radius: 15px; 
#             max-width: 70%;
#             margin-bottom: 8px;
#             align-self: flex-start;
#             font-size: 14px;
#             color: #000;
#         """
#         if sender == "You":
#             st.markdown(f'''
#                 <div style="display:flex; justify-content:flex-end;">
#                     <div style="{user_style}">
#                         <b>👤 {sender}:</b> {message}
#                     </div>
#                 </div>
#             ''', unsafe_allow_html=True)
#         else:
#             st.markdown(f'''
#                 <div style="display:flex; justify-content:flex-start;">
#                     <div style="{bot_style}">
#                         <b>🤖 {sender}:</b> {message}
#                     </div>
#                 </div>
#             ''', unsafe_allow_html=True)

#     # Chat messages container
#     chat_box = st.container()
#     chat_box.markdown(f'<div style="{chat_container_style}">', unsafe_allow_html=True)

#     # Render each message
#     for sender, msg in st.session_state.chat_history:
#         render_message(sender, msg)

#     chat_box.markdown("</div>", unsafe_allow_html=True)

#     chat_input = st.text_input(
#         "Type your question here...", 
#         key="chat_input", 
#         placeholder="Ask me about careers, skills, or advice"
#     )

#     send_button = st.button("Send", use_container_width=True)


#     # Clear chat button below input
 

#     # When user clicks send, get response and append
#     if send_button and chat_input:
#         with st.spinner("🤖 Thinking..."):
#             response = careerbot_chat(chat_input)

#         st.session_state.chat_history.append(("You", chat_input))
#         st.session_state.chat_history.append(("Bot", response))
#         st.rerun()

# # === Tab 5: About ===
# with tabs[4]:
#     st.subheader("About this project")
#     st.markdown("""
#     This AI Career Counselor was built to guide tech students by analyzing their resume skills and personality traits.
    
#     - Developed using Streamlit, OpenAI GPT, and custom skill gap analysis
#     - Generates detailed PDF career reports with learning resources
#     - Includes chatbot for interactive career advice
#     """)

import streamlit as st
from streamlit_lottie import st_lottie
import json
import importlib
from datetime import datetime
from io import BytesIO
from pathlib import Path
import traceback

# -------------------------------
# SAFE ASSET LOADER
# -------------------------------
@st.cache_data
def load_lottie(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None


career_animation = load_lottie("streamlit_app/assets/career.json")
quiz_animation = load_lottie("streamlit_app/assets/quiz.json")
resume_animation = load_lottie("streamlit_app/assets/resume.json")

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(page_title="AI Career Counselor", page_icon="🎓", layout="wide")

st.title("🎓 AI Career Counselor")
st.write("Upload your resume → Take quiz → Get your perfect career recommendation!")

# -------------------------------
# PDF Generator (Simple + Safe)
# -------------------------------
def create_pdf(skills, careers):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "Career Report", ln=True, align="C")

    pdf.set_font("Helvetica", size=12)
    pdf.ln(5)
    pdf.multi_cell(0, 8, "Extracted Skills:")
    pdf.multi_cell(0, 8, ", ".join(skills))

    pdf.ln(5)
    pdf.multi_cell(0, 8, "Recommended Careers:")
    for c in careers:
        pdf.multi_cell(0, 8, f"- {c}")

    # return PDF bytes
    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()

# -------------------------------
# TABS
# -------------------------------
tabs = st.tabs(["🏁 Introduction", "📄 Resume Upload", "🧠 Personality Quiz", "📝 Chatbot", "ℹ️ About"])

# -------------------------------
# 1️⃣ INTRO TAB
# -------------------------------
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        if career_animation:
            st_lottie(career_animation, height=250)
    with col2:
        st.write("""
        ✔ Extract skills from your resume  
        ✔ Analyze personality  
        ✔ Generate career recommendations  
        ✔ Download full PDF report  
        """)

# -------------------------------
# 2️⃣ RESUME UPLOAD TAB
# -------------------------------
with tabs[1]:
    st.subheader("📄 Upload Your Resume")

    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if uploaded_file:
        try:
            st.info("Processing your resume... please wait ⏳")

            resume_parser = importlib.import_module("resume_parser")
            result = resume_parser.extract_skills_from_pdf(uploaded_file)

            st.session_state.resume_data = result

            st.success("Resume Processed Successfully!")
            st.write("📌 **Name:**", result.get("name"))
            st.write("🎓 **Education:**", result.get("education"))
            st.write("🛠 **Skills:**")
            st.code(", ".join(result.get("skills", [])))

        except Exception as e:
            st.error("Failed to parse resume.")
            st.code(traceback.format_exc())

# -------------------------------
# 3️⃣ PERSONALITY QUIZ TAB
# -------------------------------
with tabs[2]:
    st.subheader("🧠 Personality Quiz")

    if "resume_data" not in st.session_state:
        st.warning("Upload your resume first!")
    else:
        resume_skills = st.session_state.resume_data["skills"]

        quiz = importlib.import_module("personality_quiz")
        base_q = quiz.get_quiz_questions()
        tech_q = quiz.generate_technical_questions(resume_skills)

        all_questions = base_q + tech_q

        responses = []
        for i, q in enumerate(all_questions):
            score = st.slider(q['question'], 1, 5, 3, key=f"q{i}")
            responses.append(score)

        if st.button("Recommend Careers"):
            careers = quiz.evaluate_personality(responses, all_questions)
            st.session_state.recommended_careers = careers

            st.success("Top Recommended Careers:")
            for c in careers:
                st.markdown(f"✔ **{c}**")

            pdf_data = create_pdf(resume_skills, careers)
            st.download_button("📄 Download Career Report", pdf_data,
                               file_name="career_report.pdf", mime="application/pdf")

# -------------------------------
# 4️⃣ CHATBOT TAB
# -------------------------------
with tabs[3]:
    st.subheader("🤖 Career Chatbot")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_msg = st.text_input("Ask anything about careers:")

    if st.button("Send"):
        bot = importlib.import_module("chatbot")
        reply = bot.careerbot_chat(user_msg)

        st.session_state.chat.append(("You", user_msg))
        st.session_state.chat.append(("Bot", reply))

    for s, m in st.session_state.chat:
        st.write(f"**{s}:** {m}")

# -------------------------------
# 5️⃣ ABOUT TAB
# -------------------------------
with tabs[4]:
    st.subheader("ℹ️ About")
    st.write("""
    This tool analyzes resume + personality + skills gap  
    to recommend suitable career paths in tech.
    """)

