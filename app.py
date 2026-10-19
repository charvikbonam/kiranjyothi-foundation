"""
Kiranjyothi Research Foundation - Flask backend (single file).

What it does
  * Serves the website folder (index.html, about.html, ... images/, data/).
  * Stores achievements in SQLite (data.db) and exposes a JSON API.
  * Admin API protected by a password (env ADMIN_PASSWORD) -> signed token.
  * Image uploads for achievements (saved to uploads/).
  * Contact form relay: sends messages to Telegram. The bot token never reaches the browser.

Run locally
  pip install flask itsdangerous
  export ADMIN_PASSWORD='choose-a-strong-password'
  export SECRET_KEY='a-long-random-string'
  export TELEGRAM_BOT_TOKEN='123456:ABC...'      (optional)
  export TELEGRAM_CHAT_ID='123456789'            (optional)
  python3 app.py            -> http://127.0.0.1:5000

Production: gunicorn -w 2 -b 0.0.0.0:8000 app:app
"""
import json
import os
import re
import sqlite3
import time
import urllib.parse
import urllib.request
import uuid
from datetime import date
from functools import wraps

from flask import Flask, abort, g, jsonify, request, send_from_directory
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = BASE_DIR                      # the HTML/CSS/images folder
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.environ.get('DB_PATH', os.path.join(BASE_DIR, 'data.db'))
SEED_JSON = os.path.join(BASE_DIR, 'data', 'achievements.json')

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Itismebro')
SECRET_KEY = os.environ.get('SECRET_KEY', 'Itismebro')
TG_TOKEN = os.environ.get('8991387127:AAGS8TDfqJdLr3DuV4q24YuL8uJ-kN8p54I', '')
TG_CHAT = os.environ.get('8801641740', '')
TOKEN_HOURS = 12
ALLOWED_EXT = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
CATEGORIES = {'academic', 'social', 'spiritual', 'agri', 'family', 'startups', 'general'}

app = Flask(__name__, static_folder=None)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024   # 10 MB per request
serializer = URLSafeTimedSerializer(SECRET_KEY, salt='krf-admin')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------------------------------------------------- database

def db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_):
    conn = g.pop('db', None)
    if conn is not None:
        conn.close()


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""CREATE TABLE IF NOT EXISTS achievements (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        summary TEXT NOT NULL,
        body TEXT NOT NULL,
        images TEXT NOT NULL DEFAULT '[]',
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL)""")
    count = con.execute('SELECT COUNT(*) FROM achievements').fetchone()[0]
    if count == 0 and os.path.exists(SEED_JSON):      # first run: import starter content
        now = int(time.time())
        for a in json.load(open(SEED_JSON, encoding='utf-8')):
            con.execute('INSERT OR IGNORE INTO achievements VALUES (?,?,?,?,?,?,?,?,?)',
                        (a['id'], a['title'], a['category'], a['date'], a['summary'],
                         a['body'], json.dumps(a.get('images', [])), now, now))
    con.commit()
    con.close()


def row_to_dict(r):
    return {'id': r['id'], 'title': r['title'], 'category': r['category'], 'date': r['date'],
            'summary': r['summary'], 'body': r['body'], 'images': json.loads(r['images'])}


# ---------------------------------------------------------------- auth

def make_token():
    return serializer.dumps({'role': 'admin'})


def require_admin(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        token = auth[7:] if auth.startswith('Bearer ') else ''
        try:
            data = serializer.loads(token, max_age=TOKEN_HOURS * 3600)
            if data.get('role') != 'admin':
                raise BadSignature('bad role')
        except (BadSignature, SignatureExpired):
            return jsonify(error='Please log in again.'), 401
        return view(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------- validation

def clean_text(value, field, max_len, required=True):
    value = (value or '').strip()
    if required and not value:
        raise ValueError(f'{field} is required.')
    if len(value) > max_len:
        raise ValueError(f'{field} must be at most {max_len} characters.')
    return value


def validate_achievement(data):
    category = data.get('category', 'general')
    if category not in CATEGORIES:
        raise ValueError('Unknown category.')
    d = (data.get('date') or '').strip()
    try:
        date.fromisoformat(d)
    except ValueError:
        raise ValueError('Date must be in YYYY-MM-DD format.')
    images = data.get('images', [])
    if not isinstance(images, list) or not all(isinstance(i, str) and i.startswith(('/uploads/', 'images/')) for i in images):
        raise ValueError('Invalid image list.')
    return {
        'title': clean_text(data.get('title'), 'Title', 120),
        'category': category,
        'date': d,
        'summary': clean_text(data.get('summary'), 'Summary', 220),
        'body': clean_text(data.get('body'), 'Story', 20000),
        'images': images[:12],
    }


def slugify(text):
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:40] or 'item'
    return f'{s}-{uuid.uuid4().hex[:6]}'


# ---------------------------------------------------------------- public API

@app.get('/api/achievements')
def list_achievements():
    cat = request.args.get('category')
    limit = min(int(request.args.get('limit', 100)), 200)
    sql = 'SELECT * FROM achievements'
    params = []
    if cat in CATEGORIES:
        sql += ' WHERE category = ?'
        params.append(cat)
    sql += ' ORDER BY date DESC, created_at DESC LIMIT ?'
    params.append(limit)
    return jsonify([row_to_dict(r) for r in db().execute(sql, params)])


@app.get('/api/achievements/<aid>')
def get_achievement(aid):
    r = db().execute('SELECT * FROM achievements WHERE id = ?', (aid,)).fetchone()
    if not r:
        return jsonify(error='Not found.'), 404
    return jsonify(row_to_dict(r))


# Telegram rate limit: max 5 contact messages per IP per 10 minutes (in memory).
_hits = {}

@app.post('/api/contact')
def contact():
    ip = request.remote_addr or 'unknown'
    now = time.time()
    recent = [t for t in _hits.get(ip, []) if now - t < 600]
    if len(recent) >= 5:
        return jsonify(error='Too many messages. Please try again later.'), 429
    recent.append(now)
    _hits[ip] = recent

    data = request.get_json(silent=True) or {}
    try:
        name = clean_text(data.get('name'), 'Name', 100)
        phone = clean_text(data.get('phone'), 'Phone', 60)
        topic = clean_text(data.get('topic'), 'Topic', 100, required=False) or 'General enquiry'
        msg = clean_text(data.get('message'), 'Message', 2000)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    if data.get('website'):          # honeypot field, humans never fill it
        return jsonify(ok=True)

    text = f'📩 New message from website\nName: {name}\nPhone: {phone}\nTopic: {topic}\n\n{msg}'
    if not (TG_TOKEN and TG_CHAT):
        return jsonify(error='Telegram is not configured on the server.'), 503
    try:
        payload = urllib.parse.urlencode({'chat_id': TG_CHAT, 'text': text}).encode()
        req = urllib.request.Request(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage', data=payload)
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(resp.status)
    except Exception:
        app.logger.exception('Telegram send failed')
        return jsonify(error='Could not send the message right now.'), 502
    return jsonify(ok=True)


# ---------------------------------------------------------------- admin API

@app.post('/api/login')
def login():
    pw = (request.get_json(silent=True) or {}).get('password', '')
    if pw != ADMIN_PASSWORD:
        time.sleep(1)                # slow down password guessing
        return jsonify(error='Wrong password.'), 401
    return jsonify(token=make_token(), hours=TOKEN_HOURS)


@app.post('/api/achievements')
@require_admin
def create_achievement():
    try:
        a = validate_achievement(request.get_json(silent=True) or {})
    except ValueError as e:
        return jsonify(error=str(e)), 400
    aid = slugify(a['title'])
    now = int(time.time())
    con = db()
    con.execute('INSERT INTO achievements VALUES (?,?,?,?,?,?,?,?,?)',
                (aid, a['title'], a['category'], a['date'], a['summary'], a['body'],
                 json.dumps(a['images']), now, now))
    con.commit()
    return jsonify(id=aid, **a), 201


@app.put('/api/achievements/<aid>')
@require_admin
def update_achievement(aid):
    try:
        a = validate_achievement(request.get_json(silent=True) or {})
    except ValueError as e:
        return jsonify(error=str(e)), 400
    con = db()
    cur = con.execute("""UPDATE achievements SET title=?, category=?, date=?, summary=?, body=?,
                         images=?, updated_at=? WHERE id=?""",
                      (a['title'], a['category'], a['date'], a['summary'], a['body'],
                       json.dumps(a['images']), int(time.time()), aid))
    con.commit()
    if cur.rowcount == 0:
        return jsonify(error='Not found.'), 404
    return jsonify(id=aid, **a)


@app.delete('/api/achievements/<aid>')
@require_admin
def delete_achievement(aid):
    con = db()
    cur = con.execute('DELETE FROM achievements WHERE id = ?', (aid,))
    con.commit()
    if cur.rowcount == 0:
        return jsonify(error='Not found.'), 404
    return jsonify(ok=True)


@app.post('/api/upload')
@require_admin
def upload():
    f = request.files.get('file')
    if not f or not f.filename:
        return jsonify(error='No file received.'), 400
    ext = f.filename.rsplit('.', 1)[-1].lower() if '.' in f.filename else ''
    if ext not in ALLOWED_EXT:
        return jsonify(error='Only JPG, PNG, GIF or WEBP images are allowed.'), 400
    name = f'{uuid.uuid4().hex[:10]}-{secure_filename(f.filename)[:60]}'
    f.save(os.path.join(UPLOAD_DIR, name))
    return jsonify(url=f'/uploads/{name}'), 201


@app.get('/api/export')
@require_admin
def export_all():
    """Full backup as JSON (same format as data/achievements.json)."""
    return jsonify([row_to_dict(r) for r in db().execute('SELECT * FROM achievements ORDER BY date DESC')])


# ---------------------------------------------------------------- serving the website

@app.get('/uploads/<path:name>')
def uploaded_file(name):
    return send_from_directory(UPLOAD_DIR, name)


@app.get('/')
def home():
    return send_from_directory(SITE_DIR, 'index.html')


@app.get('/<path:name>')
def site_file(name):
    # Only serve the website's own folders and pages; never the backend source or database.
    blocked = {'app.py', 'data.db', 'config.json', 'build.py', 'requirements.txt'}
    if name.split('/')[0] in {'source', '.git', '__pycache__'} or name in blocked:
        abort(404)
    if name.endswith('.py') or name.endswith('.db'):
        abort(404)
    return send_from_directory(SITE_DIR, name)


@app.errorhandler(413)
def too_big(_):
    return jsonify(error='File is too large (max 10 MB).'), 413


init_db()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=False)
