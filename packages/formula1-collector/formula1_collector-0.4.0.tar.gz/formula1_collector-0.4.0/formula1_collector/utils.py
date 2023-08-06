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

def get_practice_url(url, practice_num, practice=False):
    web = get(url)

    soup = BeautifulSoup(web.text, 'lxml')

    items = soup.find_all(class_='side-nav-item-link')
    if practice:
        if practice_num == 2 and 'Qualifying' in items[-practice_num].text:
            return items[-practice_num-1].text, 'https://www.formula1.com'+items[-practice_num-1]['href']
        elif practice_num == 3 and 'Practice 2' in items[-practice_num].text:
            return 'Error', ''
        return items[-practice_num].text, 'https://www.formula1.com'+items[-practice_num]['href']
        
    if practice_num == 4 and 'grid' in items[-practice_num].text:
        return items[-practice_num+2].text, 'https://www.formula1.com'+items[-practice_num+2]['href']
    
    return items[-practice_num].text, 'https://www.formula1.com'+items[-practice_num]['href']

def correct_string(string: str) -> str:
    if 'ü' in string or 'é' in string:
        return string.replace('ü','u').replace('é','e')
    return string