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
from flask_mail import Mail, Message
import random
import string
import datetime
from bs4 import BeautifulSoup
from datetime import datetime

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntüleme izniniz yok", "danger")
            return redirect(url_for("index"))
    return decorated_function

def send_verification_email(email, token):
    verification_link = url_for("verify_email", token=token, _external=True)
    msg = Message("Hesap Doğrulama", sender="help.dershane@gmail.com", recipients=[email])
    msg.body = f"Merhaba, hesabınızı doğrulamak için aşağıdaki linke tıklayın:\n{verification_link}"
    mail.send(msg)

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        passwordAgain = request.form.get("passwordAgain")

        cursor = mysql.connection.cursor()

        if password != passwordAgain:
            cursor.close()
            flash("Girdiğiniz şifreler birbiri ile eşleşmiyor. Lütfen tekrar deneyiniz.", "danger")
            return redirect(url_for("register"))
        
        sorgu = "SELECT * FROM users WHERE Email = %s"
        result = cursor.execute(sorgu, (email,))

        sorgu2 = "SELECT * FROM users WHERE Username = %s"
        result2 = cursor.execute(sorgu2, (username,))

        if result or result2 > 0:
            cursor.close()
            flash("Kullanıcı adınız ya da email adresiniz kullanılıyor. Lütfen başka bir isim veya mail adresi giriniz.", "danger")
            return redirect(url_for("register"))
        
        hashedPassword = sha256_crypt.encrypt(password)

        verification_token = generate_random_string(20)

        sorgu3 = "INSERT INTO users (Username, Email, Password, VerificationToken) VALUES (%s, %s, %s, %s)"
        cursor.execute(sorgu3, (username, email, hashedPassword, verification_token))

        mysql.connection.commit()
        cursor.close()

        send_verification_email(email, verification_token)

        flash("Kayıt işlemi başarıyla gerçekleşti. E-postanıza gönderdiğimiz linki kullanarak hesabınızı aktifleştirin.", "primary")
        return redirect(url_for("login"))

@app.route("/verify_email/<token>")
def verify_email(token):
    cursor = mysql.connection.cursor()

    sorgu = "SELECT * FROM users WHERE VerificationToken = %s"
    result = cursor.execute(sorgu, (token,))

    if result > 0:
        user_data = cursor.fetchone()

        sorgu2 = "UPDATE users SET IsActive = True, VerificationToken = NULL WHERE ID = %s"
        cursor.execute(sorgu2, (user_data["ID"],)) 

        mysql.connection.commit()
        cursor.close()

        flash("Hesabınız başarıyla aktifleştirildi. Giriş yapabilirsiniz.", "success")
        return redirect(url_for("login"))
    else:
        flash("Geçersiz veya süresi dolmuş bir doğrulama linki. Lütfen tekrar kayıt olun.", "danger")
        return redirect(url_for("register"))

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = mysql.connection.cursor()

        sorgu = "SELECT * FROM users where Email = %s"
        result = cursor.execute(sorgu, (email,))

        if result > 0:
            data = cursor.fetchone()

            if sha256_crypt.verify(password, data["Password"]):
                cursor.close()

                session["logged_in"] = True
                session["username"] = data["Username"]
                session["hiz"] = data["Hiz"]
                session["IsActive"] = data["IsActive"]

                flash("Hesabınıza başarıyla giriş yaptınız...", "primary")
                
                if data["IsActive"] == False:
                    flash("Lütfen mail adresinize gönderdiğimiz linke tıklayarak hesabınızı aktifleştiriniz.", "warning")
                    return redirect(url_for("index"))
                
                else:
                    if data["Hiz"] == 0:
                        return redirect(url_for("hiz"))
                    
                    else:
                        return redirect(url_for("dashboard"))
            
            else:
                flash("Şifre yanlış. Lütfen tekrar deneyiniz.", "danger")
                return redirect(url_for("login"))
        
        else:
            flash("Böyle bir kullanıcı bulunamadı. Lütfen tekrar deneyiniz.", "danger")
            return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("index.html")

@app.route("/hiz-belirleme", methods = ["GET", "POST"])
@login_required
def hiz():
    if request.method == "GET":
        return render_template("hiz.html")
    
    elif request.method == "POST":
        cursor = mysql.connection.cursor()


        if 'baslangic' in request.form:

            if session["hiz"] > 0:
                flash("Hızınız zaten belirlenmiş. Sıfırdan başlamanıza gerek yok!", "warning")
                return redirect(url_for("index"))
            
            sorgu = "UPDATE users SET Hiz = 100 WHERE Username = %s"
            cursor.execute(sorgu, (session["username"],))

            mysql.connection.commit()
            cursor.close()

            flash("Artık başlamak için hazırsınız!", "primary")
            return redirect(url_for("dashboard"))
        
        elif 'ileri' in request.form:

            if session["hiz"] > 0:
                flash("Hızınız zaten belirlenmiş. Tekrar hız belirlemenize gerek yok!", "warning")
                return redirect(url_for("dashboard"))
            
            return redirect(url_for("hizolcme"))


@app.route("/hiz-olcme", methods=["GET", "POST"])
@login_required
def hizolcme():
    if request.method == "GET":
        return render_template("hizolcme.html")

    elif request.method == "POST":

        data = request.get_json()
        reading_speed = data.get('reading_speed') 

# Burada eksik var unutma

        cursor = mysql.connection.cursor()

        sorgu = "UPDATE users SET Hiz = %s WHERE Username = %s"
        cursor.execute(sorgu, (reading_speed , session["username"]))

        mysql.connection.commit()
        cursor.close()

        flash("Okuma hızınıza göre başlangıç yeriniz ayarlandı!", "primary")
        return redirect(url_for("dashboard"))


    
@app.route("/logout")
@login_required
def logout():
    session.clear()

    flash("Çıkış yapıldı...", "primary")
    return redirect(url_for("index"))

@app.route("/kurallar")
def kurallar():
    return render_template("kurallar.html")

if __name__ == "__main__":
    app.run(debug=True)