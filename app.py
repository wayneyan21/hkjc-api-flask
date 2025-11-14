# -*- coding: utf-8 -*-
"""
Simplified Flask API for Render Deployment
"""

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import mysql.connector as mysql

# Load .env variables
load_dotenv()

# Flask app
app = Flask(__name__)
app.config.update(JSON_AS_ASCII=False, JSON_SORT_KEYS=False)
CORS(app)

# Database settings
DB_CFG = dict(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASS", ""),
    database=os.getenv("DB_NAME", "hkjc_db"),
    charset="utf8mb4"
)

# Health check
@app.get("/api/health")
def health():
    return {"ok": True}

# Horse list
@app.get("/api/horses")
def horses():
    conn = mysql.connect(**DB_CFG)
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT horse_id, name_chi, sex, age, colour, country FROM horses LIMIT 50")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

# Start server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
