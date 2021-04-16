from bs4 import BeautifulSoup, NavigableString
import requests
import datetime
import csv
import os
import schedule
import time

def make_file():
    # Check if dir already exits, create one of it does not
    if not os.path.exists('nairaland'):
        os.makedirs('nairaland')

    # Set the header for the csv file
    header = ['Title', 'Post by', 'Link']

    # Make a request for the featured contents
    html = requests.get("https://nairaland.com").text

    # Parse the response
    soup = BeautifulSoup(html, 'lxml')

    # Find the tdable_data that contains a list of anchor_elements
    result = soup.find('td', class_='featured w')

    # Set the date as the name of the file
    st = str(datetime.datetime.now().year ) + '-' + str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day)


    # Loop through the return a tags, read and write the title, user,
    # ahref of the post
    with open(f'nairaland/{st}.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in result.find_all('a'):
            title = item.extract() if isinstance(item, NavigableString) else item.text
            link = requests.get(item['href']).text
            soup = BeautifulSoup(link, 'lxml')
            a = soup.find('a', class_='user')
            writer.writerow([title, a.text, item['href']])

    print("Done")



if __name__ == '__main__':
    # Only run this code when it is 12 at night
    schedule.every().day.at('01:07:00').do(make_file)
    while True:
        schedule.run_pending()
        time.sleep(60)

