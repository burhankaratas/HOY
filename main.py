from flask import Flask,render_template,flash,redirect,url_for,session,request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
from functools import wraps
import random
import string
import datetime
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
    if "logged_in" in session:
        return redirect(url_for("dashboard"))
    
    else:
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
                session["dateTime"] = data["DateTime"]
                session["puan"] = data["Points"]
                session["email"] = data["Email"]
                session["id"] = data["ID"]
                
                if data["IlkHiz"] != 0:
                    session["ilkhiz"] = data["IlkHiz"]

                flash("Hesabınıza başarıyla giriş yaptınız...", "primary")
                
                if data["IsActive"] == False:
                    flash("Lütfen mail adresinize gönderdiğimiz linke tıklayarak hesabınızı aktifleştiriniz.", "warning")
                    return redirect(url_for("logout"))
                
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

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if request.method == "GET":
        cursor = mysql.connection.cursor()

        sorgu = "SELECT * FROM adimlar"
        cursor.execute(sorgu)

        data = cursor.fetchall()

        cursor.close()

        # Kullanıcının okuma hızına göre hangi adımdan başlayacağını belirle
        ilk_hiz = int(session.get("ilkhiz", 0))
        if ilk_hiz < 100:
            baslangic_adimi = 1
        elif 100 <= ilk_hiz < 200:
            baslangic_adimi = 2
        elif 200 <= ilk_hiz < 300:
            baslangic_adimi = 3
        elif 300 <= ilk_hiz < 400:
            baslangic_adimi = 4
        elif 400 <= ilk_hiz < 500:
            baslangic_adimi = 5
        elif 500 <= ilk_hiz < 600:
            baslangic_adimi = 6
        elif 600 <= ilk_hiz < 700:
            baslangic_adimi = 7
        elif 700 <= ilk_hiz < 800:
            baslangic_adimi = 8
        elif 800 <= ilk_hiz < 900:
            baslangic_adimi = 9
        elif 900 <= ilk_hiz < 1000:
            baslangic_adimi = 10
        elif 1000 <= ilk_hiz < 1100:
            baslangic_adimi = 11
        else:
            # Kullanıcının okuma hızı 1100'den büyükse en son adımdan başla
            baslangic_adimi = 11

        # Belirlenen adımdan sonraki verileri al
        data = data[baslangic_adimi - 1:]

        return render_template("dashboard.html", data=data)
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
            
            sorgu = "UPDATE users SET Hiz = 50, IlkHiz = 50 WHERE Username = %s"
            cursor.execute(sorgu, (session["username"],))

            session["ilkhiz"] = 50
            session["hiz"] = 50

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

        okumahizi = request.form.get('okumahizi')

        cursor = mysql.connection.cursor()

        sorgu = "UPDATE users SET Hiz = %s, IlkHiz = %s WHERE Username = %s"
        cursor.execute(sorgu, (okumahizi , okumahizi ,session["username"]))

        session["ilkhiz"] = okumahizi
        session["hiz"] = okumahizi

        mysql.connection.commit()
        cursor.close()

        flash("Okuma hızınıza göre başlangıç yeriniz ayarlandı!", "primary")
        return redirect(url_for("dashboard"))

@app.route("/profil")
@login_required
def profil():
    utc_tarih = session["dateTime"]
    utc_datetime = datetime.strptime(utc_tarih, "%a, %d %b %Y %H:%M:%S %Z")
    turkish_tarih = utc_datetime.strftime("%d %b %Y")

    return render_template("profil.html", turkish_tarih = turkish_tarih)

@app.route("/ayarlar", methods=["GET", "POST"])
@login_required
def ayarlar():
    if request.method == "GET":
        return render_template("ayarlar.html")
    
    elif request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')

        cursor = mysql.connection.cursor()

        if session["email"] != email or session["username"] != username:
            # Kullanıcı adı veya e-posta değişmişse kontrol yap
            if email:
                sorgu_email = "SELECT * FROM users WHERE Email = %s"
                cursor.execute(sorgu_email, (email,))
                data_email = cursor.fetchone()

                # E-posta başka bir kullanıcı tarafından kullanılıyorsa uyarı ver
                if data_email and data_email["ID"] != session["id"]:
                    flash("Bu e-posta adresi başka bir kullanıcı tarafından kullanılıyor.", "danger")
                    return redirect(url_for("ayarlar"))

            if username:
                sorgu_username = "SELECT * FROM users WHERE Username = %s"
                cursor.execute(sorgu_username, (username,))
                data_username = cursor.fetchone()

                # Kullanıcı adı başka bir kullanıcı tarafından kullanılıyorsa uyarı ver
                if data_username and data_username["ID"] != session["id"]:
                    flash("Bu kullanıcı adı başka bir kullanıcı tarafından kullanılıyor.", "danger")
                    return redirect(url_for("ayarlar"))

            # Eğer buraya kadar gelinmişse, güncelleme işlemini gerçekleştir
            sorgu_update = "UPDATE users SET Username = %s, Email = %s WHERE ID = %s"
            cursor.execute(sorgu_update, (username, email, session["id"]))

            session["username"] = username
            session["email"] = email
            
            mysql.connection.commit()
            cursor.close()

            flash("Kullanıcı bilgileriniz güncellendi...", "primary")
            return redirect(url_for("ayarlar"))
        
        # Eğer değişiklik yapılmamışsa uyarı ver
        else:
            flash("Herhangi bir değişiklik yapmadınız.", "warning")

        return redirect(url_for("ayarlar"))

@app.route("/1/1")
@login_required
def adim1ders1():
    # fonksiyonları cagırmada bir hata var. Düzelt
    return render_template("app/adim1ders1.html")
    

@app.route("/ilerleme", methods = ["GET"])
@login_required
def ilerleme():
    return render_template("ilerleme.html")

@app.route("/alistirmalar")
@login_required
def alistirmalar():
    return render_template("alistirmalar.html")

    
@app.route("/logout")
@login_required
def logout():
    session.clear()

    flash("Çıkış yapıldı...", "primary")
    return redirect(url_for("index"))

@app.route("/kurallar")
def kurallar():
    return render_template("kurallar.html")

@app.route("/kosullar")
def kosullar():
    return render_template("kosullar.html")

@app.route("/gizlilik")
def gizlilik():
    return render_template("gizlilik.html")

@app.route("/test")
def test():
    return render_template("karalama.html")

@app.route("/misyonumuz")
def misyonumuz():
    return render_template("misyonumuz.html")

@app.route("/sss")
def sss():
    return render_template("sss.html")

if __name__ == "__main__":
    app.run(debug=True)