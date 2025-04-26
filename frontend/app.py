# frontend/app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px  # Using Plotly for better charts

BACKEND_URL = "http://localhost:8000/analyze"  # Adjust if you deploy it

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🤖 AI-Powered Resume Analyzer")
st.write("Upload resumes and a job description to analyze fit and get improvement suggestions!")

# Upload files
st.sidebar.header("Upload Files")

resumes = st.sidebar.file_uploader(
    "Upload Resumes (PDF or DOCX)",
    type=['pdf', 'docx'],
    accept_multiple_files=True
)

job_description = st.sidebar.file_uploader(
    "Upload Job Description (PDF, DOCX, or TXT)",
    type=['pdf', 'docx', 'txt']
)

candidates = []

if st.sidebar.button("Analyze"):

    if not resumes or not job_description:
        st.warning("Please upload both resumes and a job description!")
    else:
        with st.spinner("Analyzing resumes..."):
            files = []

            # Prepare resumes
            for resume in resumes:
                files.append(("resumes", (resume.name, resume, resume.type)))

            # Prepare job description
            files.append(("job_description", (job_description.name, job_description, job_description.type)))

            response = requests.post(BACKEND_URL, files=files)

            if response.status_code == 200:
                analysis_results = response.json()

                for result in analysis_results:
                    candidates.append({
                        "Resume Name": result['filename'],
                        "Fit Score": result['fit_score'],
                        "Missing Skills": ", ".join(result['missing_skills']),
                        "Suggestions": result['improvement_suggestions']
                    })

                # Convert to DataFrame and sort by highest score
                candidates_df = pd.DataFrame(candidates)
                candidates_df = candidates_df.sort_values(by="Fit Score", ascending=False)

                # 🧩 1️⃣ Table of Candidates
                st.header("📋 Candidates Overview")
                st.dataframe(candidates_df)

                # 📈 2️⃣ Insights
                st.header("📊 Summary Insights")

                avg_score = candidates_df["Fit Score"].mean()
                top_candidates = candidates_df[candidates_df["Fit Score"] == 100]
                low_candidates = candidates_df[candidates_df["Fit Score"] < 50]

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("📈 Average Fit Score", f"{avg_score:.2f}%")

                with col2:
                    st.metric("🏅 Perfect Matches (100%)", len(top_candidates))

                with col3:
                    st.metric("⚠️ Weak Matches (<50%)", len(low_candidates))

                # 📈 3️⃣ Charts

                st.subheader("📊 Fit Score Distribution")

                fig_bar = px.bar(
                    candidates_df,
                    x="Resume Name",
                    y="Fit Score",
                    color="Fit Score",
                    color_continuous_scale="Viridis",
                    title="Fit Score per Resume"
                )
                st.plotly_chart(fig_bar, use_container_width=True)

                st.subheader("🧩 Score Ranges Pie Chart")

                def score_category(score):
                    if score >= 80:
                        return "Excellent (80-100%)"
                    elif score >= 50:
                        return "Good (50-79%)"
                    else:
                        return "Poor (<50%)"

                candidates_df['Score Category'] = candidates_df['Fit Score'].apply(score_category)

                fig_pie = px.pie(
                    candidates_df,
                    names='Score Category',
                    title='Candidate Quality Distribution'
                )
                st.plotly_chart(fig_pie, use_container_width=True)

                # 🏆 4️⃣ Best Matching Resume
                st.header("🏆 Best Matching Resume")

                best_candidate = candidates_df.iloc[0]
                st.success(f"🏆 {best_candidate['Resume Name']} (Score: {best_candidate['Fit Score']}%)")

                # ⬇️ 5️⃣ Download CSV
                st.header("⬇️ Download Candidates Data")

                csv = candidates_df.to_csv(index=False).encode('utf-8')

                st.download_button(
                    label="⬇️ Download Candidates as CSV",
                    data=csv,
                    file_name="candidates_overview.csv",
                    mime="text/csv"
                )

                # 📄 6️⃣ Detailed Analysis for Each Resume
                st.header("📄 Detailed Candidate Analysis")

                for result in analysis_results:
                    with st.expander(f"📄 {result['filename']}"):
                        st.subheader("Fit Score:")
                        st.progress(result['fit_score'] / 100)
                        st.write(f"**Score:** {result['fit_score']}%")

                        st.subheader("🔍 Missing Skills:")
                        if result['missing_skills']:
                            st.error(", ".join(result['missing_skills']))
                        else:
                            st.success("No missing skills detected!")

                        st.subheader("🛠 Suggestions for Improvement:")
                        st.info(result['improvement_suggestions'])

                        report_content = f"""
Resume: {result['filename']}
Fit Score: {result['fit_score']}%

Missing Skills: {', '.join(result['missing_skills'])}
Suggestions:
{result['improvement_suggestions']}
"""
                        st.download_button(
                            label="📥 Download Report",
                            data=report_content,
                            file_name=f"{result['filename'].split('.')[0]}_report.txt",
                            mime="text/plain"
                        )

            else:
                st.error("Something went wrong during analysis. Please try again.")
