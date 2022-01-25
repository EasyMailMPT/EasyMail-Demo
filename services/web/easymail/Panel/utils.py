import urllib, urllib.request, urllib.error, urllib.parse
import re
from easymail import app,db
from serpapi import GoogleSearch
from easymail.models import Emails, Websites
import requests



email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,3})', re.IGNORECASE)
email_regex_check = re.compile(r'^((?!jpg|png|web|gif|jpeg|svg|pdf).)*$')
url_regex = re.compile('<a\s.*?href=[\'"](.*?)[\'"].*?>')

### SERPAPI Get request #####
def create_request(keyword,country,num_results,device,domain,engine):
    params = {
    "engine": engine,
    "q": keyword,
    "num": num_results,
    "device":device,
    "domain":domain,
    "api_key": "5527926c809f659c50b17be93abe0eb7e237aba9fefee393313b0465f18fa2d7"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']
    print(organic_results)
    websites = []
    for url in organic_results:
        urls = url['link']
        websites.append(urls)
    print(websites)
    return websites
    
    


### Check if emails for keyword exists in database ###
def check_database(keyword):
    websites = Websites.query.filter_by(keyword=keyword).all()
    if websites is None:
        return 0
    else:
        for website in websites:
            return websites
        
### First depth search function
def find_emails_in_html(url, website_id):
    url_parse_retries = 2
    html = None
    for _ in range(url_parse_retries):
        try:
            html = urllib.request.urlopen(url, timeout=5)
            continue
        except urllib.error.URLError or urllib.error.HTTPError as err:
            print("Exception at url: %s\n%s" % (url, err))
            return
        except Exception:
            print('Unexpected event happened')
            return

    if not html:
        return

    text_data = str(html.read())
    if not text_data:
        return

    for email in email_regex.findall(text_data):
        if email_regex_check.match(email):
            emails = Emails(email=email, website_id=website_id)
            db.session.add(emails)
            db.session.commit()
