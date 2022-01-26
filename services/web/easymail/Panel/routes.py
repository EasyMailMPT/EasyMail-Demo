from flask import render_template, url_for, flash, redirect,request,Blueprint, send_from_directory,send_file
from easymail import app,db,bcrypt
from easymail.Panel.forms import SearchForm
from easymail.Panel.utils import check_database,create_request,find_emails_in_html
from flask_login import login_user, current_user, logout_user,login_required
from easymail.models import Websites, Emails
import pandas as pd
import time

### Setup blueprint - easier to navigate in the project
Panel=Blueprint('Panel',__name__)
ROWS_PER_PAGE=25
### Endpoints and logic to endpoints - TODO querying database should be only in models file :(
###### Panel Page ##### 
@Panel.route('/emails',methods=['GET','POST'])
@login_required 
def emails():
    page = request.args.get('page',1,type=int)
    mails = Websites.query.join(Emails, Websites.id==Emails.website_id).add_columns(Websites.url,Emails.email, Websites.keyword).filter(Websites.user_id == current_user.id).all()
    keywords = set()
    for mail in mails:
        easy = mail.keyword
        keywords.add(mail.keyword)
    
        
    return render_template('panel/emails.html',mails=mails,keywords=keywords,title="Emials")

@Panel.route('/panel/createCSV/<keyword>',methods=['GET','POST'])
@login_required
def createCSV(keyword):
    mails = Websites.query.join(Emails, Websites.id==Emails.website_id).add_columns(Websites.url,Emails.email, Websites.keyword).filter(Websites.user_id == current_user.id).filter(Websites.keyword==keyword).all()
    name = 'easymail/static/files/'+keyword+str(current_user.id)+'.csv'
    download = 'static/files/'+keyword+str(current_user.id)+'.csv'
    if keyword == "all_master_easy":
        mails = Websites.query.join(Emails, Websites.id==Emails.website_id).add_columns(Websites.url,Emails.email, Websites.keyword).filter(Websites.user_id == current_user.id).all()
        name = 'easymail/static/files/'+"all"+str(current_user.id)+'.csv'
        download = 'static/files/'+"all"+str(current_user.id)+'.csv'
    output = pd.DataFrame()
    for mail in mails:
        mail_dict = {
            "E-mal":mail.email,
             "Keyword":mail.keyword,
            "Url":mail.url,
        }
        output = output.append(mail_dict,ignore_index=True)
   
    output.to_csv(name, encoding='utf-8')
    return send_file(download, as_attachment=True)

@Panel.route('/search',methods=['GET','POST'])
@login_required
def search():
    form = SearchForm()
    mails = None
    if form.validate_on_submit():
        ### Get data from form ###
        keyword = form.keyword.data
        number = str(form.number_of_links.data)
        country = form.country.data
        device = form.device.data
        domain = form.domain.data
        engine = form.engine.data
        
        ### Check if keyword exists in database ###
        database_response = check_database(keyword)
        if database_response == None:
            serp_resp = create_request(keyword,country,number,device,domain,engine)
            for url in serp_resp:
                website = Websites(url=url,keyword=keyword,user_id=current_user.id)
                db.session.add(website)
                db.session.commit()
                website_id = Websites.query.filter_by(url=url).all()
                for id in website_id:
                    emails = find_emails_in_html(url,id.id)
        return redirect(url_for('Panel.emails'))
    return render_template('panel/search.html',form=form,title="Search")

               
