import string
from flask import Blueprint , render_template ,request,flash,redirect,url_for
from .models import *
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=="POST":
        em=request.form.get('email')
        pw=request.form.get('password')

        user=User.query.filter_by(email=em).first()
        if user:
            if check_password_hash(user.password,pw):
                flash("Logged in Successfully!",category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            if not check_password_hash(user.password,pw):
                flash('Incorrrect Password! Try Again!!!',category='error')
                return redirect(url_for('auth.login'))
        else:
            flash("No User Found,Please Sign Up",category='error')
            return redirect(url_for('auth.Sign_Up'))
        
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/Sign-Up",methods=['GET','POST'])
def Sign_Up():
    if request.method=='POST':
        nm=request.form.get('name')
        em=request.form.get('email')
        pw1=request.form.get('password1')
        pw2=request.form.get('password2')
        existing=User.query.filter_by(email=em).first()
        if existing:
            flash('Email Already Exists',category='error')
            return redirect (url_for('auth.login'))
        
        if not nm or len(nm) < 2:
            flash("Name must be at least 2 characters", category="error")
            return redirect(url_for('auth.Sign_Up'))   

        if not em or len(em) < 4:
            flash("Email too short", "error")
            return redirect(url_for('auth.Sign_Up'))

        if not pw1 or len(pw1) < 7:
            flash("Password must be at least 7 characters", category="error")
            return redirect(url_for('auth.Sign_Up'))

        if pw1!=pw2:
            flash("Password Doesn\'t match" ,category="error")
            return redirect(url_for('auth.Sign_Up'))
        lower = upper = digit = spl = False
        for A in pw1:
            if A.islower():
                lower=True
            elif A.isupper():
                upper=True
            elif A.isdigit():
                digit=True
            elif A in string.punctuation:
                spl=True
        if upper==False:
            flash("Upper Case is Missing",category='Add_it')
            return redirect(url_for('auth.Sign_Up'))
        elif lower==False:
            flash("Lower Case is Missing",category='Add_it')
            return redirect(url_for('auth.Sign_Up'))
        elif digit==False:
            flash("Digit Case is Missing",category='Add_it')
            return redirect(url_for('auth.Sign_Up'))
        elif spl==False:
            flash("Special Character is Missing",category='Add_it')
            return redirect(url_for('auth.Sign_Up'))
        else:
            new_user=User(username=nm,email=em,password=generate_password_hash(pw1,method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account Created!",category='success')
            return redirect(url_for('views.home'))            
    return render_template('signup.html')
