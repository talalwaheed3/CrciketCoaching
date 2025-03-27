from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

server = "USER\CRICKETCOACHING"
database = "CricketCoachingFYP"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)
