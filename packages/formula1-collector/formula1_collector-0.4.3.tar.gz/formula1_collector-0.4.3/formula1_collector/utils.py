import re
from bs4 import BeautifulSoup
from requests import get

def first_2_words(words):
        words_list = words.split()
        return ' '.join(words_list[:2])

def get_race_url(race_num, year):
    url = 'https://www.formula1.com/en/results.html/'+str(year)+'/races.html'
    web = get(url)
    
    url = 'https://www.formula1.com'
    soup = BeautifulSoup(web.text, 'lxml')
    races = soup.find_all(class_='resultsarchive-filter-wrap')[2]
    races = races.find_all('a')
    url += races[race_num]['href']
    return url

def correct_string(string: str):
    if 'ü' in string or 'é' in string:
        return string.replace('ü','u').replace('é','e')
    return string

def correct_table_data(url: str, race_type: str):
    web = get(url)
    
    soup = BeautifulSoup(web.content.decode('latin-1'), 'lxml')
    title = soup.find(class_='ResultsArchiveTitle')
    title = ' '.join(title.text.encode('latin-1').decode('utf-8').replace('\n', '').split())
    
    if race_type in title:
        return True
    return False
    
    