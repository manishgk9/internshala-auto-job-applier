import os
from rich import print

CONFIG_FILE = 'resume.ini'

# Create resume.ini if it doesn't exist
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write(
            '# Enter your skills\n'
            'SKILLS = """\n'
            'Python, Django, REST API, Google Cloud, AWS\n'
            'Problem Solver, Team Management Skills\n'
            '"""\n\n'
            
            '# Enter your certifications and internships\n'
            'CERTIFICATES = """\n'
            '1. Problem Solving through C\n'
            '2. Artificial Intelligence from Code Camp\n'
            '3. Machine Learning Internship at Technopheliya Solutions\n'
            '"""\n\n'
            
            '# Enter your project details\n'
            '# Tip: Use GPT models to summarize projects in bullet points.\n'
            'PROJECTS = """\n'
            '1. Flutter Chatbot\n'
            '* Built an AI-powered chatbot using Flutter for real-time interaction on mobile platforms.\n\n'
            '2. LinkedIn & PDF Analyzer\n'
            '* Developed using NLP, Gemini, FastAPI, and Celery with a responsive UI built in React, Redux Toolkit, and Tailwind CSS.\n\n'
            '3. Twitter Sentiment Analyzer\n'
            '* Built a sentiment analysis tool using Machine Learning to analyze tweets and track user behavior.\n'
            '* Frontend built with React, Redux Toolkit, and Tailwind CSS.\n\n'
            '4. Internshala Automation Project\n'
            '* Automated internship/job applications using Django and Celery.\n'
            '* Built frontend with React, Redux Toolkit, and Tailwind CSS.\n\n'
            '5. Cancer Disease Detection System\n'
            '* Designed a machine learning model to detect cancer from medical data with high accuracy.\n'
            '"""\n'
        )

    print('\n[bold green]"resume.ini"[/] has been created.\n'
          'Please open it in any editor and fill in your [bold yellow]Skills, Certificates, and Projects[/].\n'
          'Then rerun the script.\n')
    exit()

# Read and sanitize ini file
with open(CONFIG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    config_data = f.read().replace(";", "#")

# Execute the config safely
try:
    exec(config_data)
except (IndentationError, SyntaxError) as e:
    print('[bold red]Error in resume.ini:[/] Please fix the formatting (make sure multiline strings are intact).\n'
          'You can delete resume.ini and rerun the script to regenerate it.')
    exit()

# Extract fields
try:
    Skills = SKILLS
except NameError:
    print('[bold red]SKILLS not found in resume.ini[/]\n'
          'Press Enter to continue without skills or edit resume.ini and restart.')
    input()
    Skills = 'No skills specified.'

try:
    Certifications = CERTIFICATES
except NameError:
    print('[bold red]CERTIFICATES not found in resume.ini[/]\n'
          'Press Enter to continue without certifications or edit resume.ini and restart.')
    input()
    Certifications = 'No certificates provided.'

try:
    Projects = PROJECTS
except NameError:
    print('[bold red]PROJECTS not found in resume.ini[/]\n'
          'Press Enter to continue without projects or edit resume.ini and restart.')
    input()
    Projects = 'No projects provided.'
# prompt for cover letter
def form_field_question_prompt(position, skills, company, job_or_internship, about, form_container_data):
    """
    Generate a structured prompt for AI to extract and autofill form data for job/internship applications.
    """
    prompt = f"""
      You are a job application assistant AI So make sure dont give any response that not act like a not a human.

      Your job is to:
      1. Analyze the HTML form fields from this container:
      ```

      {form_container_data}

      ````

      2. Use the following context:
      - Position: {position}
      - Skills Required: {skills}
      - Company: {company}
      - Type: {job_or_internship}
      - Job Description: {about}
      - Resume Context (used only for value inference when my releted question):
         My Skills
        {Skills}
       My Projects
        {Projects}
       and My Certifications
        {Certifications}
      =

      3. Extract and return a JSON object with:
      - `unique_id`: From `id` or `name` (whichever is unique)
      - `uniq_attr`: Either `"id"` or `"name"` based on what's used
      - `label`: From label or placeholder as question
      - `type`: One of `text`, `textarea`, `select`, `radio`, `checkbox`
      - `value`: Best possible answer based on user background and question
      -  your main focus o question container except any other field is requered except cover letter and confirm_availability
      
      4- Attention if any id like name="confirm_availability" ignore that this is not nessosary
      Return response in this strict JSON format:
      ```json
      {{"cover_latter":<....>,
        "questions": [
          {{
                "unique_id":custom_question_numeric_10,
                "unique_attr":"id",
                "question": "How many months of experience do you have in Front End Development?",
                "type": "number",
                "value":"1" # value is used the output which generated by you,

            }},
            {{ 
                "unique_id":"custom_question_text_12",
                "unique_attr":"id"
                "question": "Please share a link to your portfolio/work samples for Front End Development.",
                "type": "textarea",
                "value":".."
             
            }},
            {{
                "unique_id":"radio1",
                "unique_attr":"id"
                "question": "Confirm your availability"
                "type": "option",
                "value": "yes",
            }},
            {{
                "unique_id":"custom_question_range_6474685",
                "unique_attr":"id"
                "question": "Share your knowledge in Python coding and libraries."
                "type": "select",
                "value": "4",
            }}
        ]
      }}
      """
    return prompt