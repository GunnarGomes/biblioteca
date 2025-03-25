from flask import Flask, session
from blueprints.login import bp_login
from blueprints.pg_prof import bp_professor
from blueprints.cadastros import bp_cad
from dotenv import load_dotenv
import os

load_dotenv()

seckey = os.getenv("SECRETEKEY")


app = Flask(__name__)
app.secret_key = seckey

@app.context_processor
def inject_user():
    return dict(user=session.get('user'))

app.register_blueprint(bp_login)
app.register_blueprint(bp_professor)
app.register_blueprint(bp_cad)


if __name__ == '__main__':
    ((app.run(debug=True,port=9091)))
