import requests
import re
from bs4 import BeautifulSoup

links = "https://sjpl.bibliocommons.com/v2/events?page="
urls = []

integer = int(input("Range (Not more then 215): "))

for i in range(1, integer - 1):
    link = "https://sjpl.bibliocommons.com/v2/events?page=" + str(i)
    urls.append(link)
    # print(link)

information_dict = []

for url in urls:
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    # print(soup.prettify)

    ul_element = soup.find('div', class_='content-wrapper')
    lists = ul_element.find_all('li')

    # for i in lists:
    #     print(i)

    for li in lists:
        event_title_text = li.select_one('.cp-event-title h3 a')
        if event_title_text is None:
            continue
        event_title_text = event_title_text.text
        date_string_text = li.select_one('.cp-event-date span[aria-hidden="true"]').find_next_sibling('span',  attrs={'aria-hidden': 'true'}).find_next_sibling('span',  attrs={'aria-hidden': 'true'})
        time = li.select_one('.cp-event-date span[aria-hidden="true"]').text
        if date_string_text is None:
            date_string_text = li.select_one('.cp-event-date span[aria-hidden="true"]').find_next_sibling('span', {'aria-hidden': 'true'})
            # if date_string_text is None:
            #     continue
            time_text = li.select_one('span:contains("All day")').text
            time = re.search(r"All day", time_text).group()
        date_string = date_string_text.text
        dates = re.split(r'\s+–\s+', date_string)
        start_date = re.sub(r'\w+, ', '', dates[0])
        if date_string.count(",") < 2:
            end_date = "Not mentioned"
        else:
            end_date = re.sub(r'\w+, ', '', dates[1])

        # time = li.select_one('.cp-event-date span[aria-hidden="true"]').text

        event_dict = {
            'Start Date': start_date,
            'End Date': end_date,
            'Time': time,
            'Event Name': event_title_text
        }
        information_dict.append(event_dict)

for i in information_dict:
    print(i)










