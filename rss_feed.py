from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz

url = requests.get('https://gateway.bibliocommons.com/v2/libraries/sjpl/rss/events')
# print(url)

soup = BeautifulSoup(url.content, 'xml')
# print(soup.prettify)

items = soup.find_all('item')

information_list = []
ca_tz = pytz.timezone('America/Los_Angeles')

for item in items:
    title = item.title.text
    star_date_time = item.find('bc:start_date').text.split("T")
    end_date_time = item.find('bc:end_date').text.split("T")

    start_date = datetime.strptime(star_date_time[0], '%Y-%m-%d').date()
    start_time_Z = datetime.strptime(star_date_time[1], '%H:%M:%SZ')
    start_time = start_time_Z.replace(tzinfo=pytz.utc).astimezone(ca_tz).time()
    end_date = datetime.strptime(end_date_time[0], '%Y-%m-%d').date()
    end_time_Z = datetime.strptime(end_date_time[1], '%H:%M:%SZ')
    end_time = end_time_Z.replace(tzinfo=pytz.utc).astimezone(ca_tz).time()

    start_time_str = start_time.strftime('%H:%M:%S')
    end_time_str = end_time.strftime('%H:%M:%S')
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    information_dict = {
        'Title': title,
        'Start Time': start_time_str,
        'End Time': end_time_str,
        'Start Date': start_date_str,
        'End Date': end_date_str
    }
    information_list.append(information_dict)

for info in information_list:
    print(info)
