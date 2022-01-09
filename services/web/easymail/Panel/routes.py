from flask import render_template, url_for, flash, redirect,request,Blueprint
from easymail import app,db,bcrypt
from easymail.Panel.forms import SearchForm
from easymail.Panel.utils import create_request,find_emails_in_html
from easymail.models import Keywords, Emails, check_if_keyword_in_database, get_emails_from_keyword, delete_results_of_keyword
import threading, math

THREAD_NUM = 4

### Setup blueprint - easier to navigate in the project
Panel=Blueprint('Panel',__name__)

### Endpoints and logic to endpoints - TODO querying database should be only in models file :(
###### Panel Page ##### 
@Panel.route('/panel/<keyword>',methods=['GET','POST'])
def panel(keyword, number = 0):
    #changed from horrible oneliner
    mails = get_emails_from_keyword(keyword)
    return render_template('panel/main.html', title='Panel',mails=mails)

def search_html_call(urls_list, thread_id, keyword_id):
    for i in range(math.ceil(len(urls_list)/THREAD_NUM*thread_id), math.floor(len(urls_list)/THREAD_NUM*(thread_id+1))):
        find_emails_in_html(urls_list[i], keyword_id, session=db.session)

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
            t0 = threading.Thread(target=search_html_call, args=(serp_resp, 0, keyword_id))
            t1 = threading.Thread(target=search_html_call, args=(serp_resp, 1, keyword_id))
            t2 = threading.Thread(target=search_html_call, args=(serp_resp, 2, keyword_id))
            t3 = threading.Thread(target=search_html_call, args=(serp_resp, 3, keyword_id))
            t0.start()
            t1.start()
            t2.start()
            t3.start()
            t0.join()
            t1.join()
            t2.join()
            t3.join()
            # more optimal to do at the end
            session.commit()

        return redirect(url_for('Panel.panel', keyword=keyword, number=number))
    return render_template('panel/search.html', form=form, title="Search")
                