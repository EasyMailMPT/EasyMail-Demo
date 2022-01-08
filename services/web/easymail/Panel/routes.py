from flask import render_template, url_for, flash, redirect,request,Blueprint
from easymail import app,db,bcrypt
from easymail.Panel.forms import SearchForm
from easymail.Panel.utils import create_request,find_emails_in_html
from easymail.models import Keywords, Emails, check_if_keyword_in_database, get_emails_from_keyword, delete_results_of_keyword

### Setup blueprint - easier to navigate in the project
Panel=Blueprint('Panel',__name__)

### Endpoints and logic to endpoints - TODO querying database should be only in models file :(
###### Panel Page ##### 
@Panel.route('/panel/<keyword>',methods=['GET','POST'])
def panel(keyword):
    #changed from horrible oneliner
    mails = get_emails_from_keyword(keyword)

    return render_template('panel/main.html', title='Panel',mails=mails)

@Panel.route('/search',methods=['GET','POST'])
def search():
    session = db.session
    form = SearchForm()
    mails = None
    if form.validate_on_submit():
        ### Get data from form ###
        keyword = form.keyword.data
        number = int(form.number_of_links.data)
        country = form.country.data
        
        ### Check if keyword exists in database /edited by BP###
        if not check_if_keyword_in_database(keyword, number):
            delete_results_of_keyword(keyword)
            serp_resp = create_request(keyword, country, str(number))
            key = Keywords(keyword=keyword, count=number)
            session.add(key)
            keyword_id = Keywords.query.filter_by(keyword=keyword).first()
            for url in serp_resp:
                find_emails_in_html(url, keyword_id.id)
            # more optimal to do at the end
            session.commit()

        return redirect(url_for('Panel.panel', keyword=keyword))
    return render_template('panel/search.html', form=form, title="Search")
                