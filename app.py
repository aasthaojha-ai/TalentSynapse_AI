import streamlit as st
import pandas as pd
import plotly.express as px
import time
from resume_parser import extract_text_from_pdf
from preprocessing import clean_text, extract_skills
from similarity import get_tfidf_vectors, calculate_similarity
from recommender import get_missing_skills, generate_recommendations

# Page Configuration
st.set_page_config(page_title="AI Career Copilot", page_icon="🚀", layout="wide")

# Massive Custom CSS Injection for Premium SaaS Look
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

# CSS Injection without blank lines to prevent Streamlit from rendering it as Markdown
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
/* Modern Dashboard Header */
.dash-header { background: #111827; border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 32px; margin-bottom: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); display: flex; align-items: center; gap: 24px; }
.dash-icon { font-size: 54px; background: linear-gradient(135deg, #6366F1, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.dash-title { margin:0; font-size: 32px; font-weight: 800; color:#E5E7EB; letter-spacing: -0.5px; }
.dash-subtitle { margin:8px 0 0 0; color:#94A3B8; font-size:16px; font-weight: 500; }
/* Custom Cards */
.stCard { background: #111827; border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 24px; transition: transform 0.3s ease; }
.stCard:hover { transform: translateY(-4px); }
/* Giant Gradient ATS Score */
.score-value { font-size: 72px; font-weight: 800; background: linear-gradient(90deg, #6366F1, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.1; margin: 10px 0; text-align: center; }
.score-label { font-size: 15px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; text-align: center; }
/* Skill Pills */
.pill-container { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 16px; }
.pill { padding: 8px 16px; border-radius: 999px; font-size: 14px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px; transition: all 0.2s ease; }
.pill:hover { transform: scale(1.05); box-shadow: 0 4px 10px rgba(0,0,0,0.15); }
.pill.detected { background: rgba(34,197,94,0.15); color: #22C55E; border: 1px solid rgba(34,197,94,0.3); }
.pill.missing { background: rgba(239,68,68,0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
/* Action Items */
.action-item { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 18px; margin-bottom: 12px; display: flex; align-items: center; gap: 16px; color: #E5E7EB; font-size: 15px; font-weight: 500; transition: all 0.2s ease; }
.action-item:hover { background: rgba(255,255,255,0.05); transform: translateX(4px); border-color: rgba(99,102,241,0.3); }
.action-item i { color: #6366F1; font-size: 18px; width: 24px; text-align: center; }
/* Streamlit Native Overrides */
div[data-baseweb="tab-list"] { gap: 32px; border-bottom: 2px solid rgba(255,255,255,0.05); padding-bottom: 5px; }
div[data-baseweb="tab"] { background-color: transparent !important; border: none !important; padding: 12px 0 !important; font-size: 16px; font-weight: 600; color: #94A3B8; }
div[aria-selected="true"] { color: #6366F1 !important; border-bottom: 3px solid #6366F1 !important; }
div.stButton > button:first-child { background: linear-gradient(135deg, #6366F1, #4F46E5); color: white; border-radius: 12px; font-weight: 600; font-size: 16px; border: none; padding: 24px 24px; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(99,102,241,0.25); }
div.stButton > button:first-child:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(99,102,241,0.4); }
/* Hide default streamlit headers */
header {visibility: hidden;}
</style>""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("""
<div class="dash-header">
    <div class="dash-icon"><i class="fa-solid fa-bolt"></i></div>
    <div>
        <h1 class="dash-title">AI Career Copilot</h1>
        <p class="dash-subtitle">Analyze ATS compatibility, visualize skill gaps, and optimize your resume for your target role.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for Inputs
with st.sidebar:
    st.markdown('<h2 style="color:#E5E7EB; font-size: 20px; margin-bottom: 20px; font-weight: 700;"><i class="fa-solid fa-file-arrow-up" style="color:#6366F1; margin-right:8px;"></i> Input Data</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    st.markdown("---")
    job_description = st.text_area("Paste Job Description", height=300, placeholder="E.g., Looking for Python, SQL, Power BI skills.")
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("Analyze Match", type="primary", use_container_width=True)

# Main Dashboard Logic
if analyze_button:
    if uploaded_file is not None and job_description:
        # Initialize dynamic progress bar
        progress_text = "Initializing AI analysis engine..."
        my_bar = st.progress(0, text=progress_text)
        
        # 1. Parsing & Extraction
        time.sleep(0.6)
        my_bar.progress(25, text="Extracting and cleaning text from Resume...")
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if not resume_text:
            my_bar.empty()
            st.error("❌ Failed to extract text. The PDF might be empty, corrupted, or an image without text.")
            st.stop()
            
        cleaned_resume = clean_text(resume_text)
        cleaned_jd = clean_text(job_description)
        
        # 2. Vectorization & Similarity
        time.sleep(0.6)
        my_bar.progress(50, text="Vectorizing text and computing ATS similarity score...")
        tfidf_matrix, vectorizer = get_tfidf_vectors(cleaned_resume, cleaned_jd)
        base_similarity = calculate_similarity(tfidf_matrix)
        
        # 3. Skills Analysis
        time.sleep(0.6)
        my_bar.progress(75, text="Performing NLP skill gap analysis...")
        detected_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)
        missing_skills = get_missing_skills(detected_skills, job_skills)
        
        # 4. Weighted Compatibility Scoring Logic
        if len(job_skills) > 0:
            technical_skills_score = (len(job_skills) - len(missing_skills)) / len(job_skills)
        else:
            technical_skills_score = 1.0
            
        projects_keywords = ["project", "github", "portfolio", "built", "developed"]
        projects_score = 1.0 if any(word in cleaned_resume for word in projects_keywords) else 0.0
        
        experience_keywords = ["experience", "work", "internship", "employment", "history", "role"]
        experience_score = 1.0 if any(word in cleaned_resume for word in experience_keywords) else 0.0
        
        cert_keywords = ["certification", "certificate", "certified", "course", "udemy", "coursera"]
        certification_score = 1.0 if any(word in cleaned_resume for word in cert_keywords) else 0.0
        
        overall_score = (
            0.40 * technical_skills_score +
            0.30 * projects_score +
            0.20 * experience_score +
            0.10 * certification_score
        )
        ats_score = int(round(overall_score * 100))
        
        # 5. Recommendations
        time.sleep(0.6)
        my_bar.progress(100, text="Finalizing personalized career recommendations...")
        recommendations = generate_recommendations(ats_score, missing_skills)
        time.sleep(0.4)
        
        my_bar.empty()
        
        # Dashboard Layout Configuration (Grid emulation)
        col1, col2 = st.columns([1, 2.2], gap="large")
        
        with col1:
            # ATS Score Card
            st.markdown(f"""
            <div class="stCard score-container">
                <div class="score-label"><i class="fa-solid fa-bullseye" style="color:#6366F1; margin-right:8px;"></i> Overall Match</div>
                <div class="score-value">{ats_score}%</div>
                <p style="color:#94A3B8; margin-top:15px; font-size:14px; font-weight:500;">Compatibility Probability</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive Plotly Donut Chart Card
            st.markdown('<div class="stCard" style="padding-bottom:10px;">', unsafe_allow_html=True)
            st.markdown('<h3 style="margin-top:0; color:#E5E7EB; font-size:18px; font-weight:700; text-align:center;"><i class="fa-solid fa-chart-pie" style="color:#6366F1; margin-right:8px;"></i> Tech Skills Match</h3>', unsafe_allow_html=True)
            
            if len(job_skills) > 0:
                fig = px.pie(
                    names=["Detected Skills", "Missing Skills"],
                    values=[len(detected_skills), len(missing_skills)],
                    hole=0.7,
                    color=["Detected Skills", "Missing Skills"],
                    color_discrete_map={"Detected Skills": "#6366F1", "Missing Skills": "#1F2937"}
                )
                fig.update_traces(textinfo='none', hoverinfo='label+value')
                fig.add_annotation(text=f"{len(detected_skills)} / {len(job_skills)}<br><b>Skills</b>", 
                                   x=0.5, y=0.5, font_size=18, showarrow=False, font=dict(color="#E5E7EB"))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=20, b=10, l=0, r=0), 
                    showlegend=True, 
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(color="#94A3B8"))
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No explicit skills requested in the Job Description.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Styled Tabs
            tab1, tab2, tab3 = st.tabs([
                "🛠️ Skill Gap Analysis", 
                "💡 AI Suggestions", 
                "📋 Action Plan"
            ])
            
            with tab1:
                col_found, col_missing = st.columns(2)
                
                with col_found:
                    st.markdown("<h4 style='color:#E5E7EB; font-weight:600; margin-bottom:15px; font-size:18px;'><i class='fa-solid fa-check-circle' style='color:#22C55E; margin-right:8px;'></i> Detected Skills</h4>", unsafe_allow_html=True)
                    if detected_skills:
                        pills_html = '<div class="pill-container">'
                        for skill in detected_skills:
                            pills_html += f'<span class="pill detected"><i class="fa-solid fa-check"></i> {skill.title()}</span>'
                        pills_html += '</div>'
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='color:#94A3B8;'>No predefined skills detected.</p>", unsafe_allow_html=True)
                        
                with col_missing:
                    st.markdown("<h4 style='color:#E5E7EB; font-weight:600; margin-bottom:15px; font-size:18px;'><i class='fa-solid fa-times-circle' style='color:#EF4444; margin-right:8px;'></i> Missing Skills</h4>", unsafe_allow_html=True)
                    if missing_skills:
                        pills_html = '<div class="pill-container">'
                        for skill in missing_skills:
                            pills_html += f'<span class="pill missing"><i class="fa-solid fa-xmark"></i> {skill.title()}</span>'
                        pills_html += '</div>'
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.2); padding:16px; border-radius:12px;">
                            <p style="color:#22C55E; margin:0; font-weight:600;"><i class="fa-solid fa-award"></i> Perfect Match!</p>
                            <p style="color:#22C55E; margin:5px 0 0 0; font-size:14px; opacity:0.8;">You possess all requested skills.</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tab2:
                st.markdown("<h4 style='color:#E5E7EB; font-weight:600; margin-bottom:20px; font-size:18px;'><i class='fa-solid fa-lightbulb' style='color:#F59E0B; margin-right:8px;'></i> AI Career Advisor</h4>", unsafe_allow_html=True)
                # Dynamic recommendations HTML
                recs_html = ""
                for rec in recommendations:
                    recs_html += f'<div class="action-item"><i class="fa-solid fa-arrow-right"></i> <span>{rec}</span></div>'
                st.markdown(recs_html, unsafe_allow_html=True)
            
            with tab3:
                st.markdown("<h4 style='color:#E5E7EB; font-weight:600; margin-bottom:20px; font-size:18px;'><i class='fa-solid fa-list-check' style='color:#6366F1; margin-right:8px;'></i> Optimization Checklist</h4>", unsafe_allow_html=True)
                st.markdown("""
                <div class="action-item"><i class="fa-solid fa-pen-nib"></i> <span><b>Rewrite weak bullet points</b> to highlight direct impact and quantifiable results.</span></div>
                <div class="action-item"><i class="fa-solid fa-magnifying-glass"></i> <span><b>Add ATS keywords</b> natively into your experience and summary sections.</span></div>
                <div class="action-item"><i class="fa-solid fa-code"></i> <span><b>Improve project descriptions</b> with clear technical outcomes and architectures.</span></div>
                <div class="action-item"><i class="fa-solid fa-bullseye"></i> <span><b>Enhance summary section</b> to instantly align with the job's core requirements.</span></div>
                <div class="action-item"><i class="fa-solid fa-chart-line"></i> <span><b>Quantify achievements</b> using metrics, percentages, and solid business numbers.</span></div>
                <div class="action-item"><i class="fa-solid fa-wand-magic-sparkles"></i> <span><b>Tailor for target job</b> by mirroring the exact language and tone of the job description.</span></div>
                """, unsafe_allow_html=True)
                
    else:
        st.markdown("""
        <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.2); padding:16px; border-radius:12px; margin-top:20px;">
            <p style="color:#EF4444; margin:0; font-weight:600;"><i class="fa-solid fa-triangle-exclamation"></i> Action Required</p>
            <p style="color:#EF4444; margin:5px 0 0 0; font-size:14px; opacity:0.9;">Please upload a resume and paste a job description before analyzing.</p>
        </div>
        """, unsafe_allow_html=True)
        
elif uploaded_file is None and not job_description:
    st.markdown("""
    <div style="background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.2); padding:30px; border-radius:20px; margin-top:40px; text-align:center;">
        <i class="fa-solid fa-arrow-pointer" style="font-size:36px; color:#6366F1; margin-bottom:15px;"></i>
        <h3 style="color:#E5E7EB; margin:0; font-weight:700;">Ready to optimize your resume?</h3>
        <p style="color:#94A3B8; margin:10px 0 0 0; font-size:15px;">Upload your PDF and paste a target job description in the sidebar to get started.</p>
    </div>
    """, unsafe_allow_html=True)
