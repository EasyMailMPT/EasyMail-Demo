from flask import render_template, url_for, flash, redirect,request,Blueprint
from easymail import app,db,bcrypt
from easymail.Panel.forms import SearchForm
from easymail.Panel.utils import check_database,create_request,find_emails_in_html
from flask_login import login_user, current_user, logout_user,login_required
from easymail.models import Websites, Emails, UserEmails

### Setup blueprint - easier to navigate in the project
Panel=Blueprint('Panel',__name__)
ROWS_PER_PAGE=25
### Endpoints and logic to endpoints - TODO querying database should be only in models file :(
###### Panel Page ##### 
@Panel.route('/emails',methods=['GET','POST'])
@login_required 
def emails():
    userEmails = UserEmails.query.filter_by(user_id=current_user.id).all()
   
    return render_template('panel/emails.html',userEmails=userEmails,title="Emials")


@Panel.route('/panel/<keyword>',methods=['GET','POST'])
@login_required
def panel(keyword):
    page = request.args.get('page',1,type=int)
    mails = Websites.query.join(Emails, Websites.id==Emails.website_id).add_columns(Websites.url,Emails.email).filter(Websites.keyword==keyword).paginate(page=page,per_page=ROWS_PER_PAGE)
    web = Websites.query.filter_by(keyword=keyword).all()
    for website in web:
            ii = website.id
            emails = Emails.query.filter_by(website_id=ii).all()
    if request.method == "POST":
        websites = Websites.query.filter_by(keyword=keyword).all()
        for email in emails:
            for websiteses in websites:
                userEmails = UserEmails(keyword=keyword, email=email.email, website=websiteses.url, user_id = current_user.id)
                db.session.add(userEmails)
        db.session.commit()
        return redirect(url_for('Panel.emails'))
            
    return render_template('panel/main.html', title='Panel',mails=mails,keyword=keyword)


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
                website = Websites(url=url,keyword=keyword)
                db.session.add(website)
                db.session.commit()
                website_id = Websites.query.filter_by(url=url).all()
                for id in website_id:
                    emails = find_emails_in_html(url,id.id)
        return redirect(url_for('Panel.panel',keyword=keyword))
    return render_template('panel/search.html',form=form,title="Search")

               
