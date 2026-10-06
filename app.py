"""Compare the skills in a resume with a job description."""

import io
import re

import PyPDF2
import streamlit as st


SKILLS = [
    "Python", "Java", "C", "C++", "JavaScript", "HTML", "CSS", "React",
    "Angular", "Node.js", "Django", "Flask", "FastAPI", "SQL", "MySQL",
    "PostgreSQL", "MongoDB", "Oracle", "Git", "GitHub", "Docker", "Linux",
    "AWS", "Azure", "Google Cloud", "Pandas", "NumPy", "Matplotlib",
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "TensorFlow", "PyTorch", "Scikit-learn", "REST API", "Data Structures",
    "Algorithms", "Computer Networks", "Operating Systems", "DBMS",
]

ALIASES = {
    "ML": "Machine Learning",
    "AI": "Artificial Intelligence",
    "JS": "JavaScript",
    "ReactJS": "React",
    "NodeJS": "Node.js",
}


def extract_resume_text(pdf_file):
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.getvalue()))
        if reader.is_encrypted and not reader.decrypt(""):
            raise ValueError("This PDF is password protected.")
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except ValueError:
        raise
    except Exception as error:
        raise ValueError("Could not read this PDF. Please upload a valid PDF.") from error


def find_skills(text):
    found = set()
    for skill in SKILLS:
        terms = [skill] + [
            alias for alias, name in ALIASES.items() if name == skill
        ]
        for term in terms:
            pattern = (
                r"(?<![\w+#])C(?![\w+#])"
                if term == "C"
                else rf"(?<!\w){re.escape(term)}(?!\w)"
            )
            if re.search(pattern, text, re.IGNORECASE):
                found.add(skill)
                break
    return found


st.set_page_config(page_title="AI-Based Resume Skill Gap Analyzer")
st.title("AI-Based Resume Skill Gap Analyzer")

resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the job description")

if st.button("Analyze", type="primary"):
    if resume_file is None:
        st.error("Please upload a resume PDF.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        try:
            resume_text = extract_resume_text(resume_file)
        except ValueError as error:
            st.error(str(error))
        else:
            if not resume_text:
                st.error("No readable text found. Please upload a text-based PDF.")
            else:
                resume_skills = find_skills(resume_text)
                required_skills = find_skills(job_description)
                matching_skills = resume_skills & required_skills
                missing_skills = required_skills - resume_skills

                if required_skills:
                    score = round(len(matching_skills) / len(required_skills) * 100, 1)
                    st.metric("Skill Match Score", f"{score:g}%")
                else:
                    st.metric("Skill Match Score", "N/A")
                    st.warning("No recognized skills found in the job description.")

                for title, skills in (
                    ("Resume Skills", resume_skills),
                    ("Required Skills", required_skills),
                    ("Matching Skills", matching_skills),
                    ("Missing Skills", missing_skills),
                ):
                    st.subheader(title)
                    st.write(", ".join(skill for skill in SKILLS if skill in skills) or "None")

                st.subheader("Recommendations")
                if missing_skills:
                    for skill in SKILLS:
                        if skill in missing_skills:
                            st.write(f"Consider learning {skill}.")
                else:
                    st.write("No missing skills.")
