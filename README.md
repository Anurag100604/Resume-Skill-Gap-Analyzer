# AI-Based Resume Skill Gap Analyzer

## Objective

Compare the technical skills detected in a resume PDF with the skills mentioned
in a job description. The app shows matching skills, missing skills, a Skill
Match Score, and a simple recommendation for each missing skill.

## Features

- Upload a text-based resume PDF.
- Paste a job description and analyze it with one click.
- Extract text from all PDF pages with PyPDF2.
- Detect skills using case-insensitive keyword matching and simple aliases.
- Compare skills with Python sets and calculate a score from 0 to 100%.
- Show friendly messages for missing inputs, unreadable PDFs, and descriptions
  without recognizable skills.

The project uses straightforward text processing. It does not use machine
learning, deep learning, external APIs, or a professional ATS scoring system.

## Technologies

- Python
- Streamlit
- PyPDF2
- Python standard library (`re` and `io`)

## How it works

1. Upload a resume PDF and paste a job description.
2. `extract_resume_text(pdf_file)` reads the text from every page.
3. `find_skills(text)` checks both texts against the editable skill list in
   `app.py`, including aliases such as `ML` and `JS`.
4. Python sets are used to find the matching and missing skills.
5. The Skill Match Score is calculated as:

   `(matching required skills / total required skills) * 100`

   The score is rounded to one decimal place. If no known skills are found in
   the job description, the app shows a warning and does not calculate a score.
6. The results include recommendations for missing skills.

## Project structure

```text
.
├── app.py
├── requirements.txt
├── README.md
└── sample/
    └── sample_job_description.txt
```

## Installation

In a terminal opened in the project folder, run:

```powershell
python -m pip install -r requirements.txt
```

## How to run

```powershell
python -m streamlit run app.py
```

Streamlit prints a local address to open in your browser. Stop the application
with `Ctrl+C` in the terminal.

## Example input

Resume text in a text-based PDF:

```text
Skills: Python, SQL, Git, HTML, CSS, JavaScript, Pandas
Experience: Web development with Django and MySQL
```

Job description (also available in `sample/sample_job_description.txt`):

```text
We are looking for a Python Developer with experience in Python, SQL, Git,
Docker and AWS. Knowledge of REST API and Machine Learning is an advantage.
```

## Example output

For the example above:

- Resume skills detected: 9
- Required skills detected: 7
- Matching skills: Python, SQL, Git
- Missing skills: Docker, AWS, REST API, Machine Learning
- Skill Match Score: 42.9% — Partial Skill Match

The app also gives one learning recommendation for each missing skill.

## Limitations

- Matching is based on a fixed keyword list and does not understand context.
- Only the skills listed in `app.py` (and their aliases) can be detected.
- Scanned PDFs containing only images do not have extractable text.
- Resume sections and skill proficiency are not analyzed.
- The app does not save uploaded resumes or analysis results in a database.

## Future improvements

- Add more skills and carefully chosen aliases to the editable list.
- Support other document formats, such as DOCX.
- Detect resume sections and provide more detailed, explainable feedback.
- Add optional visualizations for comparing skills.
