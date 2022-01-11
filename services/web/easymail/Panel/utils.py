import urllib, urllib.request, urllib.error, urllib.parse
import re
from easymail import app,db
from serpapi import GoogleSearch
from easymail.models import Emails, Keywords
import requests


email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,3})', re.IGNORECASE)
email_regex_check = re.compile(r'^((?!jpg|png|web|gif|jpeg|svg|pdf).)*$')
url_regex = re.compile('<a\s.*?href=[\'"](.*?)[\'"].*?>')


### SERPAPI Get request #####
def create_request(keyword, country, num_results):
    serp_url = "http://api.serpstack.com/search?access_key=c1001e0f112fb0f38c66faf1da6532c4&query="+keyword+"&num="+num_results+"&gl="+country+"&hl="+country
    response = requests.get(serp_url)
    organic_results = response.json()['organic_results']
    websites = []
    for url in organic_results:
        urls = url['url']
        websites.append(urls)
    return websites


### First depth search function
def find_emails_in_html(url, keyword_id):
    session = db.create_scoped_session({'bind':db.engine})
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

    emails = set(email_regex.findall(text_data))
    for email in emails:
        if email_regex_check.match(email):
            email_to_send = Emails(email=email,website=url, keyword_id=keyword_id)
            session.add(email_to_send)
    session.commit() #BP: better at the end (optimal)
