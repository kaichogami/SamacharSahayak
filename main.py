import datetime

import boto3 as boto3
import pytz
from get_html.get_html import get_html_string
from scrapper.the_hindu import TheHinduScrapper
import time

DATE = datetime.datetime.now(tz=pytz.timezone('Asia/Kolkata')).strftime("%Y/%m/%d")

def get_the_hindu_html_template() -> str:
    with open("template/the_hindu.html", 'r') as f:
        the_hindu_html_string = f.read()
    return the_hindu_html_string

def write_html(html_string: str):
    with open("/home/asish/Documents/the_hindu_{}.html".format(DATE.replace("/", '-')), 'w') as f:
        f.write(html_string)

def write_to_s3(html_string):
    s3 = boto3.resource("s3")
    object = s3.Object('samachaar', 'TheHindu/{}.html'.format(DATE.replace('/', '-')))
    object.put(Body=html_string)

def main(event, handler):
    hindu_scrapper = TheHinduScrapper(DATE)
    all_content = hindu_scrapper.get_all_content()
    html_string = get_html_string(get_the_hindu_html_template(), all_content)
    write_to_s3(html_string)


if __name__ == '__main__':
    now = time.time()
    main({}, {})
    print("time taken :{}".format(time.time() - now))