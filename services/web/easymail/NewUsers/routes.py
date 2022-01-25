from flask import render_template, url_for, flash, redirect,request,Blueprint
from easymail import app,db,bcrypt
from easymail.NewUsers.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from easymail.models import User
from flask_login import login_user, current_user, logout_user,login_required
from easymail.NewUsers.utils import generate_confirmation_token, confirm_token,send_email
from flask_mail import Mail, Message
import datetime
NewUsers=Blueprint('NewUsers',__name__)


###### Login Page ##### 
@NewUsers.route('/login',methods=['GET','POST'])

def login():
    error=None
    if current_user.is_authenticated:
        return redirect(url_for('Panel.search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.confirmed == True:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Panel.search'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and user.confirmed == True and user.role=="admin":
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Admin.admin'))
        else:
            error="Nieprawidłowe hasło lub email"        
    return render_template('auth/login.html', title='Login', form=form,error=error)


###### Register Page ######
@NewUsers.route("/register", methods=['GET', 'POST'])
def register():
    error=None
    if current_user.is_authenticated:
        return redirect(url_for('Panel.search'))
    form = RegistrationForm()
    print("gti")
    if request.method == "POST":
        print("xd")
        if form.validate_on_submit():
            print("elo")
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data,email=form.email.data, password=hashed_password, confirmed=True)
            db.session.add(user)
            db.session.commit()
        
            return redirect(url_for("NewUsers.login"))
        
    return render_template('auth/register.html', title='Register', form=form,error=error)



@NewUsers.route("/verification/expired/<email>",methods=['GET', 'POST'])
def expired(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('NewUsers.confirm_email', token=token, _external=True)
    html = render_template('main/email.html', confirm_url=confirm_url)
    subject = "🚨 Zweryfikuj swoje konto | easymailmedical.pl"
    send_email(email, subject, html)
    return redirect(url_for("NewUsers.verification"))

@NewUsers.route("/verification", methods=['GET', 'POST'])
def verification():
    return render_template('main/verification.html',title='Verification')

@NewUsers.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if email == False:
        flash('Link do weryfikacji wygasł.', 'danger')
        return redirect(url_for('NewUsers.login'))
    else:
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            flash('Konto już zweryfikowane', 'success')
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            flash('Zweryfikowałeś swoje konto. Dziękujemy!', 'success')
        return redirect(url_for('NewUsers.login'))

######## RESET PASSWORD #######
def send_reset_email(user):
    token = user.get_reset_token()
    reset_link = url_for('NewUsers.reset_token', token=token, _external=True)
    subject = "Resetowanie hasła - easymailmedical.pl"
    html = render_template("main/reset_token_email.html",reset_link=reset_link)
    print(user.email)
    send_email(user.email,subject,html)


@NewUsers.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('Account.panel'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Wysłaliśmy do Ciebie maila z linkiem do resetowania hasła - sprawdź swoją skrzynkę email','success')
        return redirect(url_for('NewUsers.login'))
    return render_template('main/reset_request.html', title='Reset Password', form=form)


@NewUsers.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
 
    if current_user.is_authenticated:
        return redirect(url_for('Account.panel'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Link do resetowania hasła wygasł. Zresetuj hasło jeszcze raz', 'error')
        return redirect(url_for('NewUsers.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Twoje hasło zostało zaktualizowane', 'success')
        return redirect(url_for('NewUsers.login'))
    return render_template('main/reset_password.html', title='Reset Password', form=form)



######## LOGOUT ###########
@NewUsers.route('/logout')
def logout():
    logout_user()
    return redirect('login')
