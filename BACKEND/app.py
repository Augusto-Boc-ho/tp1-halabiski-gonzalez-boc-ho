from flask import flask
from flask_cors import CORS

app = Flask(__name__)
port = 5000
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')