# frontend/app.py
import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://localhost:8000/analyze"  # Adjust if you deploy it

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🤖 AI-Powered Resume Analyzer")
st.write("Upload resumes and a job description to analyze fit and get improvement suggestions!")

# Upload files
st.sidebar.header("Upload Files")
resumes = st.sidebar.file_uploader("Upload Resumes (PDF or DOCX)", type=['pdf', 'docx'], accept_multiple_files=True)
job_description = st.sidebar.file_uploader("Upload Job Description (TXT)", type=['txt'])

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

                # Display results
                scores = []
                filenames = []

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

                        # Allow download report
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

                    # For charts
                    filenames.append(result['filename'])
                    scores.append(result['fit_score'])

                # Fit Score Chart
                st.subheader("📊 Fit Score Overview")
                df_scores = pd.DataFrame({
                    "Resume": filenames,
                    "Fit Score": scores
                })

                st.bar_chart(df_scores.set_index("Resume"))

            else:
                st.error("Something went wrong during analysis. Please try again.")
