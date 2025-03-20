from flask import Flask
from blueprints.login import bp_login
from blueprints.pg_prof import bp_professor
from blueprints.cadastros import bp_cad
from dotenv import load_dotenv
import os

load_dotenv()

seckey = os.getenv("SECRETEKEY")


app = Flask(__name__)
app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30'

app.register_blueprint(bp_login)
app.register_blueprint(bp_professor)
app.register_blueprint(bp_cad)


if __name__ == '__main__':
    (app.run(debug=True,port=9091))
