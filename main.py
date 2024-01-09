from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,g,abort,send_file,make_response, Blueprint
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators, SubmitField, EmailField, IntegerField
from passlib.hash import sha512_crypt
from flask_mail import Mail, Message
from functools import wraps
from urllib.parse import urlencode
import random
import smtplib
import hashlib
import pdfkit


app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'help.dershane@gmail.com'
app.config['MAIL_PASSWORD'] = 'fxpg luef dcpo cbhw'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "att"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

app.secret_key = "wp+6#vfg0y3zg^ybi1u=yr)iny5seqf1$oy#7(hg5u!%2-4jv3"


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)