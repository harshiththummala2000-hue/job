from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

DB_PATH = "jobs.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                job_type TEXT NOT NULL,
                description TEXT NOT NULL,
                salary TEXT,
                contact_email TEXT NOT NULL,
                posted_at TEXT NOT NULL
            )
        """)
        conn.commit()


@app.route("/")
def index():
    query = request.args.get("q", "")
    location = request.args.get("location", "")
    job_type = request.args.get("job_type", "")

    with get_db() as conn:
        sql = "SELECT * FROM jobs WHERE 1=1"
        params = []

        if query:
            sql += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
        if location:
            sql += " AND location LIKE ?"
            params.append(f"%{location}%")
        if job_type:
            sql += " AND job_type = ?"
            params.append(job_type)

        sql += " ORDER BY posted_at DESC"
        jobs = conn.execute(sql, params).fetchall()

    return render_template("index.html", jobs=jobs, query=query, location=location, job_type=job_type)


@app.route("/job/<int:job_id>")
def job_detail(job_id):
    with get_db() as conn:
        job = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if job is None:
        flash("Job not found.", "error")
        return redirect(url_for("index"))
    return render_template("job_detail.html", job=job)


@app.route("/post", methods=["GET", "POST"])
def post_job():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        company = request.form.get("company", "").strip()
        location = request.form.get("location", "").strip()
        job_type = request.form.get("job_type", "").strip()
        description = request.form.get("description", "").strip()
        salary = request.form.get("salary", "").strip()
        contact_email = request.form.get("contact_email", "").strip()

        errors = []
        if not title:
            errors.append("Job title is required.")
        if not company:
            errors.append("Company name is required.")
        if not location:
            errors.append("Location is required.")
        if not job_type:
            errors.append("Job type is required.")
        if not description:
            errors.append("Job description is required.")
        if not contact_email:
            errors.append("Contact email is required.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("post_job.html", form=request.form)

        with get_db() as conn:
            conn.execute(
                """INSERT INTO jobs (title, company, location, job_type, description, salary, contact_email, posted_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (title, company, location, job_type, description, salary, contact_email,
                 datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()

        flash("Job posted successfully!", "success")
        return redirect(url_for("index"))

    return render_template("post_job.html", form={})


@app.route("/job/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    with get_db() as conn:
        conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
    flash("Job listing deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
