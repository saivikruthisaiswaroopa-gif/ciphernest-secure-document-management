import os
import sqlite3
import uuid
from pathlib import Path
from functools import wraps

from flask import (
    Flask, request, redirect, url_for, session,
    flash, send_file, abort, render_template_string
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# -------------------- APP CONFIGURATION --------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "documents"
DATABASE = BASE_DIR / "database.db"

UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB


# -------------------- DATABASE --------------------

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                original_name TEXT NOT NULL,
                stored_name TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                UNIQUE(document_id, user_id),
                FOREIGN KEY (document_id) REFERENCES documents(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)


def record_activity(db, document_id, action):
    db.execute(
        """INSERT INTO audit_logs (document_id, user_id, action)
           VALUES (?, ?, ?)""",
        (document_id, session["user_id"], action)
    )


# -------------------- LOGIN CHECK --------------------

def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper


# -------------------- SIMPLE PAGE DESIGN --------------------

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Document Access System</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6fb;
               margin: 35px; color: #222; }
        .container { max-width: 900px; margin: auto; background: white;
                     padding: 25px; border-radius: 12px; }
        h1, h2 { color: #263b70; }
        input, button { padding: 10px; margin: 6px 0; }
        button { background: #263b70; color: white; border: 0;
                 border-radius: 5px; cursor: pointer; }
        a { color: #2456a6; margin-right: 12px; }
        .message { background: #e8f4e8; padding: 10px; margin: 8px 0; }
        .document { border: 1px solid #ddd; padding: 12px;
                    margin: 10px 0; border-radius: 7px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 9px; text-align: left; }
        th { background: #edf0f8; }
    </style>
</head>
<body>
<div class="container">
    {% for message in get_flashed_messages() %}
        <div class="message">{{ message }}</div>
    {% endfor %}
    CONTENT
</div>
</body>
</html>
"""


def page(content, **values):
    return render_template_string(
        PAGE.replace("CONTENT", content), **values
    )


# -------------------- REGISTER --------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or len(username) > 50:
            flash("Enter a username (maximum 50 characters).")
        elif len(password) < 8:
            flash("Password must contain at least 8 characters.")
        else:
            try:
                with get_db() as db:
                    db.execute(
                        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                flash("Account created. Please log in.")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("That username already exists.")

    return page("""
        <h1>Create Account</h1>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <br>
            <input name="password" type="password"
                   placeholder="Password (at least 8 characters)" required>
            <br>
            <button type="submit">Register</button>
        </form>
        <a href="/login">Already have an account? Login</a>
    """)


# -------------------- LOGIN --------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with get_db() as db:
            user = db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        flash("Incorrect username or password.")

    return page("""
        <h1>Login</h1>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <br>
            <input name="password" type="password" placeholder="Password" required>
            <br>
            <button type="submit">Login</button>
        </form>
        <a href="/register">Create a new account</a>
    """)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------- DASHBOARD --------------------

@app.route("/")
@login_required
def dashboard():
    user_id = session["user_id"]

    with get_db() as db:
        documents = db.execute("""
            SELECT DISTINCT d.*, u.username AS owner_name
            FROM documents d
            JOIN users u ON u.id = d.owner_id
            LEFT JOIN permissions p ON p.document_id = d.id
            WHERE d.owner_id = ? OR p.user_id = ?
            ORDER BY d.id DESC
        """, (user_id, user_id)).fetchall()

    content = """
        <h1>Secure Document Dashboard</h1>
        <p>Welcome, <b>{{ username }}</b>!</p>

        <h2>Upload a Document</h2>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="document" required>
            <button type="submit">Upload</button>
        </form>

        <h2>Documents You Can Access</h2>
        {% for doc in documents %}
            <div class="document">
                <b>{{ doc.original_name }}</b><br>
                Owner: {{ doc.owner_name }}<br><br>
                <a href="/download/{{ doc.id }}">Download</a>
                {% if doc.owner_id == user_id %}
                    <a href="/share/{{ doc.id }}">Manage Access</a>
                {% endif %}
            </div>
        {% else %}
            <p>No documents found. Upload your first document.</p>
        {% endfor %}

        <hr>
        <a href="/audit">View Audit Logs</a>
        <a href="/logout">Logout</a>
    """
    return page(content, username=session["username"],
                documents=documents, user_id=user_id)


# -------------------- UPLOAD --------------------

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    uploaded_file = request.files.get("document")

    if not uploaded_file or not uploaded_file.filename:
        flash("Please choose a file.")
        return redirect(url_for("dashboard"))

    original_name = secure_filename(uploaded_file.filename)
    if not original_name:
        flash("Invalid file name.")
        return redirect(url_for("dashboard"))

    stored_name = uuid.uuid4().hex
    file_path = UPLOAD_FOLDER / stored_name
    uploaded_file.save(file_path)

    try:
        with get_db() as db:
            cursor = db.execute("""
                INSERT INTO documents (owner_id, original_name, stored_name)
                VALUES (?, ?, ?)
            """, (session["user_id"], original_name, stored_name))

            record_activity(db, cursor.lastrowid, "UPLOAD")
    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    flash("Document uploaded successfully.")
    return redirect(url_for("dashboard"))


# -------------------- ACCESS CHECK --------------------

def find_accessible_document(db, document_id):
    return db.execute("""
        SELECT d.*
        FROM documents d
        LEFT JOIN permissions p ON p.document_id = d.id
        WHERE d.id = ?
          AND (d.owner_id = ? OR p.user_id = ?)
    """, (document_id, session["user_id"], session["user_id"])).fetchone()


# -------------------- DOWNLOAD --------------------

@app.route("/download/<int:document_id>")
@login_required
def download(document_id):
    with get_db() as db:
        document = find_accessible_document(db, document_id)

        if document is None:
            abort(403)

        file_path = UPLOAD_FOLDER / document["stored_name"]
        if not file_path.is_file():
            abort(404)

        record_activity(db, document_id, "DOWNLOAD")
        original_name = document["original_name"]

    return send_file(
        file_path,
        as_attachment=True,
        download_name=original_name
    )


# -------------------- SHARE ACCESS --------------------

@app.route("/share/<int:document_id>", methods=["GET", "POST"])
@login_required
def share(document_id):
    with get_db() as db:
        document = db.execute("""
            SELECT * FROM documents
            WHERE id = ? AND owner_id = ?
        """, (document_id, session["user_id"])).fetchone()

        if document is None:
            abort(404)

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            target_user = db.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()

            if target_user is None:
                flash("User not found. Ask them to register first.")
            elif target_user["id"] == session["user_id"]:
                flash("You are already the document owner.")
            else:
                db.execute("""
                    INSERT OR IGNORE INTO permissions (document_id, user_id)
                    VALUES (?, ?)
                """, (document_id, target_user["id"]))
                record_activity(db, document_id, "ACCESS_GRANTED")
                flash("Access granted to " + username + ".")

        permissions = db.execute("""
            SELECT p.id AS permission_id, u.username
            FROM permissions p
            JOIN users u ON u.id = p.user_id
            WHERE p.document_id = ?
            ORDER BY u.username
        """, (document_id,)).fetchall()

    return page("""
        <h1>Manage Document Access</h1>
        <p>Document: <b>{{ document.original_name }}</b></p>

        <h2>Grant Access</h2>
        <form method="POST">
            <input name="username" placeholder="Registered username" required>
            <button type="submit">Grant Access</button>
        </form>

        <h2>Users With Access</h2>
        {% for person in permissions %}
            <p>
                {{ person.username }}
                <a href="/revoke/{{ document.id }}/{{ person.permission_id }}">
                    Revoke access
                </a>
            </p>
        {% else %}
            <p>No other users have access.</p>
        {% endfor %}
        <a href="/">Back to Dashboard</a>
    """, document=document, permissions=permissions)


# -------------------- REVOKE ACCESS --------------------

@app.route("/revoke/<int:document_id>/<int:permission_id>")
@login_required
def revoke(document_id, permission_id):
    with get_db() as db:
        document = db.execute("""
            SELECT id FROM documents
            WHERE id = ? AND owner_id = ?
        """, (document_id, session["user_id"])).fetchone()

        if document is None:
            abort(404)

        permission = db.execute("""
            SELECT id FROM permissions
            WHERE id = ? AND document_id = ?
        """, (permission_id, document_id)).fetchone()

        if permission:
            db.execute(
                "DELETE FROM permissions WHERE id = ?", (permission_id,)
            )
            record_activity(db, document_id, "ACCESS_REVOKED")
            flash("Document access revoked.")

    return redirect(url_for("share", document_id=document_id))


# -------------------- AUDIT LOGS --------------------

@app.route("/audit")
@login_required
def audit():
    user_id = session["user_id"]

    with get_db() as db:
        logs = db.execute("""
            SELECT a.action, a.created_at, d.original_name, u.username
            FROM audit_logs a
            JOIN documents d ON d.id = a.document_id
            JOIN users u ON u.id = a.user_id
            WHERE d.owner_id = ?
               OR EXISTS (
                    SELECT 1 FROM permissions p
                    WHERE p.document_id = d.id AND p.user_id = ?
               )
            ORDER BY a.id DESC
        """, (user_id, user_id)).fetchall()

    return page("""
        <h1>Audit Logs</h1>
        <p>Recorded document activities visible to your account.</p>
        <table>
            <tr>
                <th>Document</th>
                <th>User</th>
                <th>Action</th>
                <th>Date and Time</th>
            </tr>
            {% for log in logs %}
                <tr>
                    <td>{{ log.original_name }}</td>
                    <td>{{ log.username }}</td>
                    <td>{{ log.action }}</td>
                    <td>{{ log.created_at }}</td>
                </tr>
            {% else %}
                <tr><td colspan="4">No activity recorded yet.</td></tr>
            {% endfor %}
        </table>
        <br>
        <a href="/">Back to Dashboard</a>
    """, logs=logs)


# -------------------- ERROR PAGES --------------------

@app.errorhandler(403)
def forbidden(error):
    return page("""
        <h1>Access Denied</h1>
        <p>You are not authorized to access this document.</p>
        <a href="/">Back to Dashboard</a>
    """), 403


@app.errorhandler(404)
def not_found(error):
    return page("""
        <h1>Not Found</h1>
        <p>The requested page or document does not exist.</p>
        <a href="/">Back to Dashboard</a>
    """), 404


@app.errorhandler(413)
def file_too_large(error):
    return page("""
        <h1>File Too Large</h1>
        <p>Maximum upload size is 16 MB.</p>
        <a href="/">Back to Dashboard</a>
    """), 413


# -------------------- START SERVER --------------------

initialize_database()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
