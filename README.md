# Student Placement & Skill Tracker

A web application built with Flask that helps students manage their technical skills and track job applications in one place.

🔗 **Live Demo:** [Student Placement & Skill Tracker](https://student-placement-tracker-8hzh.onrender.com/)

## Features

- **User Authentication:** Register, log in, and log out securely.
- **Skill Management:** Add, view, edit, and delete skills.
- **Job Application Tracking:** Record and manage job applications.
- **Application Status:** Track statuses such as Applied, Online Assessment, Interview, Shortlisted, Rejected, and Selected.
- **User-Specific Data:** Keep skills and applications associated with the relevant user.
- **Database Integration:** Store application data using SQLAlchemy and PostgreSQL in the deployed application.
- **Responsive Interface:** Navigate the application through an HTML and CSS interface.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL, SQLite
- **ORM:** Flask-SQLAlchemy
- **Frontend:** HTML, CSS, Jinja2
- **Authentication:** Flask sessions, password hashing
- **Deployment:** Render
- **Database Hosting:** Neon PostgreSQL
- **Version Control:** Git and GitHub

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kamakshi1210/student-placement-tracker.git
cd student-placement-tracker
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project's root directory:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///placement_tracker.db
```

Replace `your-secret-key` with a securely generated random value. The SQLite URL is intended for local development; the deployed application uses the PostgreSQL connection URL configured in Render.

**Important:** Never commit your `.env` file or publish your database credentials.

### 5. Run the application

```bash
python run.py
```

Open the local URL displayed in your terminal, usually:

```text
http://127.0.0.1:5000/
```

## Deployment

The application is deployed on Render, with PostgreSQL hosted by Neon.

The deployment uses environment variables for configuration and Gunicorn as the production application server.

- **Live Application:** https://student-placement-tracker-8hzh.onrender.com/
- **GitHub Repository:** https://github.com/kamakshi1210/student-placement-tracker

## Learning Outcomes

This project provided practical experience with:

- Building a web application using Flask and Python.
- Implementing CRUD operations.
- Working with relational databases and SQLAlchemy.
- Implementing authentication and user-specific data access.
- Managing configuration through environment variables.
- Using Git and GitHub for version control.
- Deploying a Flask application with PostgreSQL.

## Author

**Kamakshi Barskar**

- GitHub: [@kamakshi1210](https://github.com/kamakshi1210)

---

*Built as a hands-on project to learn backend development, database integration, and deployment.*