from datetime import time
import logging
import sys
import os
import json_logging
import psycopg2

from flask import Flask, render_template


def get_db_connection():
    postgres_host = os.environ['DB_HOST'] or 'valpg'
    postgres_db = os.environ['DB_NAME'] or 'flask_db'
    postgres_port = os.environ['DB_PORT'] or 5432
    postgres_user = os.environ['DB_USERNAME'] or 'appuser'
    postgres_pass = os.environ['DB_PASSWORD'] or 'securepass'
    conn = psycopg2.connect(host=postgres_host,
                            port=postgres_port,
                            database=postgres_db,
                            user=postgres_user,
                            password=postgres_pass)
    return conn


app = Flask(__name__)
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("valogger")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tournament ORDER BY points DESC;')
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/win/<player>')
def win_player(player):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "UPDATE tournament SET points=points+3 WHERE player='" + player + "';"
    cur.execute(query)
    conn.commit()
    cur.execute('SELECT * FROM tournament ORDER BY points DESC;')
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/draw/<player>')
def draw_player(player):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "UPDATE tournament SET points=points+1 WHERE player='" + player + "';"
    cur.execute(query)
    conn.commit()
    cur.execute('SELECT * FROM tournament ORDER BY points DESC;')
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/add/<player>')
def add_player(player):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "INSERT INTO tournament (player, points) values ('" + player + "', 0);"
    cur.execute(query)
    conn.commit()
    cur.execute('SELECT * FROM tournament ORDER BY points DESC;')
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/drop/<player>')
def drop_player(player):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "DELETE FROM tournament WHERE player='" + player + "';"
    cur.execute(query)
    conn.commit()
    cur.execute('SELECT * FROM tournament ORDER BY points DESC;')
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/restart')
def restart():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tournament SET points=0;')
    conn.commit()
    cur.execute('SELECT * FROM tournament ORDER BY points DESC;')
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/reset')
def reset():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('TRUNCATE tournament;')
    conn.commit()
    cur.execute('SELECT * FROM tournament ORDER BY points DESC;')
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/ping')
def ping():
    return "pong\n"
