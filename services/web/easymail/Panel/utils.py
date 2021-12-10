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
def create_request(keyword,country,num_results):
    serp_url = "http://api.serpstack.com/search?access_key=c1001e0f112fb0f38c66faf1da6532c4&query="+keyword+"&num="+num_results+"&gl="+country+"&hl="+country
    response = requests.get(serp_url)
    organic_results = response.json()['organic_results']
    websites = []
    for url in organic_results:
        urls = url['url']
        websites.append(urls)
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
def find_emails_in_html(url,website_id):
    try:
        html = urllib.request.urlopen(url)
    except urllib.error.URLError or urllib.error.HTTPError as err:
        print("Exception at url: %s\n%s" % (url, err))
        html = urllib.request.urlopen("http://natolin15.pl")
    except Exception:
        print('Unexpected event happened')
        html = urllib.request.urlopen("http://natolin15.pl")
    text_data = str(html.read())

    if not text_data:
        return set()
    # email_list = set()
    for email in email_regex.findall(text_data):
        if email_regex_check.match(email):
            emails = Emails(email=email, website_id=website_id)
            db.session.add(emails)
            db.session.commit()
