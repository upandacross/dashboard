from flask import Flask, render_template
from dashboard_app import create_dash_app

# Create Flask app
app = Flask(__name__)

# Create and integrate Dash app with Flask
dash_app = create_dash_app()
dash_app.init_app(app)

@app.route("/")
def hello_world():
    return render_template("index.html")
