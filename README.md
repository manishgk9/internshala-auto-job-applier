# Internshala Auto Job Applier

> Automate your Internshala job applications with intelligent job matching, bulk applications, AI-generated assignments, and professional cover letters — powered by Django, DRF, Celery, Selenium, and Google Gemini AI.

![License](https://img.shields.io/github/license/manishgk9/internshala-auto-job-applier)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)

---

## 📹 Demo Video
[![Watch on YouTube](https://img.shields.io/badge/Watch%20on%20YouTube-red?logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=t_i9CGHBuNU)


https://github.com/user-attachments/assets/d41a2e97-ee41-432d-b5da-3801f6f9b1f6

---

## 📖 Overview

Internshala Auto Job Applier is a full-stack automation tool that integrates:

- **Job Matching & Filtering** — Finds jobs aligned with your skills/interests.
- **Bulk Apply** — Apply to multiple positions with one click.
- **Queue Processing** — Add jobs to a queue for automatic scheduled applications.
- **AI Integration** — Uses Gemini AI to solve assignments and write tailored cover letters.
- **Selenium Automation** — Interacts with Internshala in real time without detection.

This tool is designed to **save hours of manual effort** for frequent Internshala applicants while ensuring **personalized and professional applications**.

---

## 🚀 Features

- **Get All Matching Jobs** — Automatically scrape and filter jobs based on your profile and saved preferences.
- **Apply to Specific Jobs** — Select individual jobs and apply instantly.
- **Bulk Apply** — Select multiple jobs and apply to them in one batch operation.
- **Search Jobs by Query** — Keyword-based job search with advanced filtering.
- **Apply via Queue** — Add selected jobs to an application queue and let Celery handle the rest.
- **Auto Assignment Solver** — Automatically complete skill/aptitude tests using Gemini AI.
- **AI Cover Letter Generator** — Creates job-specific cover letters with a professional tone.
- **Undetectable Automation** — Uses `undetected-chromedriver` to avoid detection by Internshala's bot checks.
- **Task Scheduling** — Automate periodic searches and applications.

---

## 💡 Use Cases

- **Time-Saver** for applicants applying to multiple jobs daily.
- **Hands-Free Applications** for those with a busy schedule.
- **Quality Applications** with AI-generated cover letters and assignment answers.
- **High Throughput** by processing multiple jobs in parallel.

---

## 🛠 Tech Stack

### **Backend**

- **Django** — Core backend framework
- **Django REST Framework (DRF)** — API layer
- **JWT Authentication** — Secure token-based authentication
- **Gemini AI API** — NLP-powered assignment solver and cover letter generator
- **Celery** — Background task processing
- **Redis** — Message broker for Celery
- **Selenium** — Browser automation for applying to jobs
- **undetected-chromedriver** — Prevents bot detection during Selenium automation

### **Frontend**

- **React (Vite)** — High-performance SPA frontend
- **Redux Toolkit** — State management
- **Axios** — API requests
- **Tailwind CSS** — Styling framework
- **Chart.js** — (Optional) For any visual analytics

---

## 📂 Folder Structure

```

internshala-auto-job-applier/
│
├── backend/
│   ├── api/                        # DRF API endpoints
│   ├── backend/                    # Settings, configurations
│   ├── internshala_scraper/        # Selenium-based application scripts
│   ├── celery.py                   # Celery tasks
│   ├── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── redux/         # Redux slices
│   │   ├── App.jsx        # main
│   └── store.js           # store
└── README.md

```

---

## 🔗 Routes

### **Frontend Pages**

- `/` — Home page
- `/login` — Authentication
- `/dashboard` — Overview of applications and job stats
- `/search` — Search jobs by keywords and filters
- `/queue` — View and manage queued jobs

### **Backend API (DRF)**

- `GET /api/get-matching-jobs/` — Fetch jobs matching profile
- `GET /api/search-query/<str:query>` — Search jobs by query
- `POST /api/apply` — Apply to a single job or many
- `GET /api/applied-jobs/` — Applied jobs

---

## ⚙ Installation

### **Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Run Celery worker:

```bash
celery -A backend worker -l info
```

### **Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

## ⚠ Disclaimer

This project is for **educational and personal use only**.
Automating applications on Internshala may violate their terms of service.
The developer assumes **no liability** for misuse.

---

## 👤 About Developer

**Manish Yadav** — Full Stack Developer specializing in automation, AI integration, and productivity tools.
[GitHub](https://github.com/manishgk9)

- 💼 [LinkedIn](https://www.linkedin.com/in/manishgk9)
- 🐦 [Twitter/X](https://x.com/manishgk9)
- 💻 [GitHub](https://github.com/manishgk9)

> For collaboration, issues, or improvements, feel free to open a PR or contact me!

---

## 📜 License

Licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```

```
