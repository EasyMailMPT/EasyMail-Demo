from flask import render_template, url_for, flash, redirect,request,Blueprint
from easymail import app,db,bcrypt
Main=Blueprint('Main',__name__)


###### Main Page ##### 
@Main.route('/',methods=['GET','POST'])

def main():
    return redirect(url_for('NewUsers.login'))
