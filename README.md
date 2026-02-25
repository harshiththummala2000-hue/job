# JobBoard

A simple job board web application built with Python and Flask.

## Features

- Browse and search job listings by keyword, location, and job type
- View full job details
- Post new job listings
- Delete listings

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open http://localhost:5000 in your browser.

## Project Structure

```
job/
├── app.py              # Flask app — routes, models, DB logic
├── requirements.txt
├── static/
│   └── style.css       # Styles
└── templates/
    ├── base.html       # Shared layout
    ├── index.html      # Job listings + search
    ├── job_detail.html # Single job view
    └── post_job.html   # Post a new job
```

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via Python's built-in `sqlite3`)
- **Frontend:** Jinja2 templates, plain CSS
