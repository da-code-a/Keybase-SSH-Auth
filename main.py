"""
Keybase SSH Authentication Server
Copyright 2019 - Donald Brown, dkb@shrt.email
Published under the MIT License

This module is the main module in this project. It
runs the Flask server responsible for requesting,
checking, and reporting SSH authentication requests.
"""

from flask import Flask, jsonify, request
from models import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import path, environ
from functions import channel, bot_name, send_auth_request, find_first_reaction, send_decision
from datetime import datetime

load_dotenv()

db_path = path.dirname(path.abspath(__file__)) + '/data.db'
db_uri = 'sqlite:///' + db_path
if not path.exists(db_path):
    from models import init_db
    init_db(db_uri)

engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.flask_env = environ['FLASK_ENV']

@app.before_request
def check_auth():
    """
    This function checks each request for the auth
    key to be present in the request before
    allowing it to continue.
    """
    if request.values.get('token') != environ['AUTH_TOKEN']:
        return "Unauthorized", 401

@app.route('/request', methods=['POST'])
def new_request():
    """
    This function receives a request from the PAM script and
    returns a request ID used for later checking.
    """
    user = request.values.get('user')
    server = request.values.get('server')
    remote = request.values.get('remote')
    now = datetime.now()
    msg_id = send_auth_request(server, remote, user)
    conn = Session()
    new_req = Request(
        user = user,
        host = server,
        msg_id = msg_id,
        request_ts = now,
        remote = remote,
        decider = None,
        decision = None,
        decision_ts = None
    )
    conn.add(new_req)
    conn.commit()
    conn.close()
    return str(msg_id)

@app.route('/check/<path:msg_id>', methods=['GET'])
def check_status(msg_id):
    """
    This function checks the current status
    of a request based on msg_id and returns
    pending, approved, or denied as a string
    to the PAM script to decide whether to
    continue checking, send a time-out request,
    or exit with the appropriate status code.
    """
    decision, decider = find_first_reaction(int(msg_id))
    if not decision:
        return 'pending'
    else:
        conn = Session()
        saved_req = conn.query(Request).filter(Request.msg_id == int(msg_id)).first()
        saved_req.decision_ts = datetime.now()
        saved_req.decision = decision
        saved_req.decider = decider
        conn.commit()
        send_decision(False, decider, decision, saved_req.user, saved_req.host, saved_req.remote, saved_req.msg_id)
        conn.close()
        return decision

@app.route('/timeout', methods=['POST'])
def timeout():
    """
    This function records a timeout from the PAM
    script. Saves it in the DB as a timeout and
    sends a chat message letting you know that
    it was timed out and automatically denied.
    """
    msg_id = int(request.values.get('msg_id'))
    conn = Session()
    saved_req = conn.query(Request).filter(Request.msg_id == int(msg_id)).first()
    saved_req.decision_ts = datetime.now()
    saved_req.decision = 'timed_out'
    saved_req.decider = 'automatic - time_out'
    conn.commit()
    send_decision(True, saved_req.decider, saved_req.decision, saved_req.user, saved_req.host, saved_req.remote, saved_req.msg_id)
    conn.close()
    return 'OK'

if __name__ == '__main__':
    app.run()