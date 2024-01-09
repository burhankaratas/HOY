from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,g,abort,send_file,make_response, Blueprint
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators, SubmitField, EmailField, IntegerField
from passlib.hash import sha512_crypt, sha256_crypt
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
app.config["MYSQL_DB"] = "hokuveay"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

app.secret_key = "wp+6#vfg0y3zg^ybi1u=yr)iny5seqf1$oy#7(hg5u!%2-4jv3"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordAgain = request.form.get('passwordAgain')

        cursor = mysql.connection.cursor()

        if password != passwordAgain:
            cursor.close()
            flash("Girdiğiniz şifreler birbiri ile eşleşmiyor. Lütfen tekrar deneyiniz.", "danger")
            return redirect(url_for("register"))
        
        sorgu = "SELECT * FROM users where Email = %s"
        result = cursor.execute(sorgu, (email,))

        sorgu2 = "SELECT * FROM users where Username = %s"
        result2 = cursor.execute(sorgu2, (username,))

        if result or result2 > 0:
            cursor.close()
            flash("Kullanıcı adınız ya da email adresiniz kullanılıyor. Lütfen başka bir isim veya mail adresi giriniz.", "danger")
            return redirect(url_for("register"))
        
        hashedPassword = sha256_crypt.encrypt(password)

        sorgu3 = "INSERT INTO users (Username, Email, Password) VALUES (%s, %s, %s)"
        cursor.execute(sorgu3, (username, email, hashedPassword))

        mysql.connection.commit()
        cursor.close()

        flash("Kayıt işlemi başarıyla gerçekleşti...", "primary")
        return redirect(url_for("hiz"))

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        pass


@app.route("/hiz-belirleme", methods = ["GET", "POST"])
def hiz():
    if request.method == "GET":
        return render_template("hiz.html")
    

@app.route("/kurallar")
def kurallar():
    return render_template("kurallar.html")

if __name__ == "__main__":
    app.run(debug=True)