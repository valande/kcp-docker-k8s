from datetime import time
import logging
import sys
import os
import json_logging
import psycopg2

from flask import Flask, render_template


def get_db_connection():
    conn = psycopg2.connect(dbname=db_name,
                            user=db_user,
                            password=db_pass,
                            host=db_host,
                            port=db_port)
    return conn

def player_exists(player):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT count(*) FROM tournament where player = '" + player + "'"
    cur.execute(query)
    playerdb = cur.fetchone()
    cur.close()
    conn.close()
    return (int(playerdb[0]) == 1)


db_name = os.environ['DB_NAME'] or 'flask_db'
db_user = os.environ['DB_USERNAME'] or 'dbuser'
db_pass = os.environ['DB_PASSWORD'] or 'dbpass'
db_host = os.environ['DB_HOSTNAME'] or 'database'
db_port = os.environ['DB_PORT'] or 5432

app = Flask(__name__)
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)
logger = logging.getLogger("valogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT * FROM tournament ORDER BY points DESC;"
    cur.execute(query)
    tournament = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tournament=tournament)

@app.route('/win/<player>')
def win_player(player):
    if player_exists(player):
        conn = get_db_connection()
        cur = conn.cursor()
        logger.debug("+3 points to " + player)
        query = "UPDATE tournament SET points=points+3 WHERE player='" + player + "';"
        cur.execute(query)
        conn.commit()
        conn.close()
    return index()

@app.route('/draw/<player>')
def draw_player(player):
    if player_exists(player):
        conn = get_db_connection()
        cur = conn.cursor()
        logger.debug("+1 point to " + player)
        query = "UPDATE tournament SET points=points+1 WHERE player='" + player + "';"
        cur.execute(query)
        conn.commit()
        conn.close()
    return index()

@app.route('/add/<player>')
def add_player(player):
    if not player_exists(player):
        conn = get_db_connection()
        cur = conn.cursor()
        logger.debug("Add player " + player)
        query = "INSERT INTO tournament (player, points) values ('" + player + "', 0);"
        cur.execute(query)
        conn.commit()
        conn.close()
    return index()

@app.route('/drop/<player>')
def drop_player(player):
    if player_exists(player):
        conn = get_db_connection()
        cur = conn.cursor()
        logger.debug("Delete player " + player)
        query = "DELETE FROM tournament WHERE player='" + player + "';"
        cur.execute(query)
        conn.commit()
        conn.close()
    return index()

@app.route('/restart')
def restart():
    conn = get_db_connection()
    cur = conn.cursor()
    logger.debug("Restart tournament")
    cur.execute('UPDATE tournament SET points=0;')
    conn.commit()
    conn.close()
    return index()

@app.route('/reset')
def reset():
    conn = get_db_connection()
    cur = conn.cursor()
    logger.debug("Reset tournament")
    cur.execute('TRUNCATE tournament;')
    conn.commit()
    conn.close()
    return index()
