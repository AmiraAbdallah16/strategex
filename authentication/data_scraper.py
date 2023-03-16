import os
import csv
import shutil
import requests
from bs4 import BeautifulSoup

def scrape_data(country,Contents):

    url = f'https://www.cia.gov/the-world-factbook/countries/{country}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # geography
    # economy
    all = soup.findChild('div',class_="free-form-content__content wysiwyg-wrapper wfb-nav-article",id=f'{Contents}')



    Content = all.findChildren('div')

    texts_array=[]

    for divs in Content:
        texts=[]

        try:
            texts.append(divs.find_all('h3', class_='mt30')[0].text.strip())
            data = str(divs.find_all('p')[0])
            br_separated = data.split("<br/>") 
            br_separated = [x.strip() for x in br_separated] # to remove any leading or trailing whitespaces

            # now br_separated contains an array of strings, where each string is the text between two <br/> tags
            for text in br_separated:
                cleared_text = BeautifulSoup(text,'html.parser')
                cleared_text = cleared_text.get_text()
                texts.append(cleared_text)
            my_list = [x for x in texts if x] # remove empty strings

            # print(my_list)
            texts_array.append(my_list)
        except:
            continue


    # Write data to a CSV file
    with open(f'countryData/{country}_{Contents}.csv', "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for text in texts_array:
            writer.writerow(text)

    # Get the path to the downloads folder
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    # Move the file from the current location to the downloads folder
    shutil.move(f'countryData/{country}_{Contents}.csv', os.path.join(downloads_folder, f'{country}_{Contents}.csv'))
