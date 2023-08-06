import pandas as pd
import xml.etree.ElementTree as ET
from requests import get
from bs4 import BeautifulSoup
from .utils import first_2_words, get_race_url, correct_string, correct_table_data


def get_drivers(year):
    '''
    param: year
    
    returns all de drivers who ran the desired year
    
    return: pandas dataframe ['driver_id', 'driver_num', 'name', 'date_birth', 'nationality', 'picture']
    '''
    url = 'http://ergast.com/api/f1/'+str(year)+'/drivers'
    web = get(url)
    root = ET.XML(web.text)
    table_drivers = list(root)
    table_drivers = table_drivers[0]

    drivers = []
    for driver in table_drivers:
        drivers.append([driver.attrib['driverId'],0,'','','',driver.attrib['url']])
        for j, items in enumerate(driver):
            if j == 0:
                drivers[-1][1] = int(items.text)
            elif j == 1:
                drivers[-1][2] = items.text
            elif j == 2:
                drivers[-1][2] = ' '.join([drivers[-1][2],items.text])
            else:
                drivers[-1][j] = items.text
    
    return pd.DataFrame(drivers,columns=['driver_id', 'driver_num', 'name', 'date_birth', 'nationality', 'picture'])


def get_driver_info(driver: str) -> dict:
    '''
    Giving a driver name returns all the information of the driver
    
    return: dict with the information
    '''
    driver = correct_string(driver)
    
    url = 'https://www.formula1.com/en/drivers.html'
    web = get(url)
    soup = BeautifulSoup(web.text, 'lxml')
    items = soup.find_all(class_='listing-item--link')
    url = ''
    for item in items:
        list_str = item['data-tracking'].split()
        pos = 0
        for i, element in enumerate(list_str):
            if 'path' in element:
                pos = i
                break
        name = ' '.join(list_str[4:pos+3]).replace("'",'').replace('"','').replace(',','')
        
        if name == driver:
            url = 'https://www.formula1.com' + item['href']

    if not url:
        return {}
    
    web = get(url)
    soup = BeautifulSoup(web.text, 'lxml')
    
    items2 = soup.find_all(class_='stat-key')
    if not items2:
        return {}
    titles = [x.span.text for x in items2]

    items3 = soup.find_all(class_='stat-value')
    attributes = [x.text for x in items3]

    result = {}
    for num, title in enumerate(titles):
        title = title.replace(' ', '_')
        if title != 'Date_of_birth':
            result[title] = attributes[num].encode("latin-1").decode("utf-8")
    
    return result
    

def get_teams(year):
    '''
    param: year
    
    returns all the teams who participate in the desired year
    
    return: pandas dataframe ['team_id', 'name', 'nationality', 'picture']
    '''
    url = 'http://ergast.com/api/f1/'+str(year)+'/constructors'

    web = get(url)
    root = ET.XML(web.text)
    table_teams = list(root)
    table_teams = table_teams[0]

    teams = []
    for team in table_teams:
        teams.append([team.attrib['constructorId'],'','',team.attrib['url']])
        for j, items in enumerate(team):
            teams[-1][j+1] = items.text
                
    return pd.DataFrame(teams,columns=['team_id', 'name', 'nationality', 'picture'])
    

def get_calendar():
    '''
    return the calendar of races in the current year.
    
    return: pandas dataframe ['id', 'race_name', 'circuit_id', 'circuit_name', 'location', 'date_race', 'hour_race',
                              'date_practice_1', 'hour_practice_1', 'date_practice_2', 'hour_practice_2', 'date_practice_3',
                              'hour_practice_3', 'date_pool', 'hour_pool']
    '''
    url = 'http://ergast.com/api/f1/current'

    web = get(url)
    root = ET.XML(web.text)
    table_circuits = list(root)
    table_circuits = table_circuits[0]

    circuits = []
    for circuit in table_circuits:
        circuits.append([circuit.attrib['round'],'','','','','','','','','','','','','',''])
        for j, item in enumerate(circuit):
            if j == 0:
                circuits[-1][j+1] = item.text
                
            elif j == 1:
                circuits[-1][j+1] = item.attrib['circuitId']
                for k, value in enumerate(item):
                    if k == 0:
                        circuits[-1][3] = value.text
                    else:
                        for z, location in enumerate(value):
                            if z == 0:
                                circuits[-1][4] = location.text
                            else:
                                circuits[-1][4] += ' (' + location.text + ')'
            
            elif j == 2 or j == 3:
                circuits[-1][j+3] = item.text
            
            else:
                k = j+2+j-4+1
                for z, dates in enumerate(item):
                    circuits[-1][k+z] = dates.text
                
    return pd.DataFrame(circuits,columns=['id', 'race_name', 'circuit_id', 'circuit_name', 'location', 'date_race', 'hour_race',
                                          'date_practice_1', 'hour_practice_1', 'date_practice_2', 'hour_practice_2', 'date_practice_3',
                                          'hour_practice_3', 'date_pool', 'hour_pool'])


def get_classification(year):
    '''
    param: year
    
    return the clasification of a desired year
    
    return: pandas dataframe ['Pos','Driver','Nationality','Car','PTS']
    '''
    url = 'https://www.formula1.com/en/results.html/'+str(year)+'/drivers.html'

    table = pd.read_html(url)

    table[0]['Driver'] = table[0]['Driver'].apply(first_2_words)
    
    return table[0][['Pos','Driver','Nationality','Car','PTS']]


def get_classification_by_team(year):
    '''
    param: year
    
    get the classification of the teams in a specific year
    
    return: pandas dataframe ['Pos','Team','PTS']
    '''
    url = 'https://www.formula1.com/en/results.html/'+str(year)+'/team.html'

    table = pd.read_html(url)

    return table[0][['Pos','Team','PTS']]


def get_starting_grid(race_num, year):
    '''
    params: race_num, year
    
    Given a race num (numer of the race in the given year) and a year returns the starting grid.
    
    return: pandas dataframe ['race_id', 'Pos', 'Driver', 'Car']
    '''
    url = get_race_url(race_num, year)
    
    splitted_url = url.split('/')
    splitted_url[-1] = 'starting-grid.html'
    url = '/'.join(splitted_url)
    
    try:
        table = pd.read_html(url)
    except ValueError:
        return None
    
    if not correct_table_data(url,'STARTING GRID'):
        return None
    
    table[0]['Driver'] = table[0]['Driver'].apply(first_2_words)
    
    race_id = [race_num]*table[0].shape[0]
    table[0].insert(0, column = 'race_id', value = race_id)
    
    return table[0][['race_id', 'Pos', 'Driver', 'Car']]


def get_race_results(race_num, year):
    '''
    params: race_num, year
    
    returns the results of the desired race
    
    return: pandas dataframe ['race_id', 'Pos', 'Driver', 'Car', 'Laps', 'Time_Retired', 'PTS']
    '''
    url = get_race_url(race_num, year)
    
    try:
        table = pd.read_html(url)
    except ValueError:
        return None
    
    if not correct_table_data(url,'RACE RESULT'):
        return None
    
    table[0]['Driver'] = table[0]['Driver'].apply(first_2_words)
    table[0].rename(columns = {'Time/Retired':'Time_Retired'}, inplace = True)
    
    race_id = [race_num]*table[0].shape[0]
    table[0].insert(0, column = 'race_id', value = race_id)
    
    return table[0][['race_id', 'Pos', 'Driver', 'Car', 'Laps', 'Time_Retired', 'PTS']]


def get_fastest_lap(race_num, year):
    '''
    params: race_num, year
    
    returns the classification by the fastest lap por specific race
    
    return: pandas dataframe ['race_id', 'Pos', 'Driver', 'Car', 'Lap', 'Time_of_day', 'Time', 'Avg_Speed']
    '''
    url = get_race_url(race_num, year)

    splitted_url = url.split('/')
    splitted_url[-1] = 'fastest-laps.html'
    url = '/'.join(splitted_url)
    
    try:
        table_fastest_lap = pd.read_html(url)
    except ValueError:
        return None
    
    if not correct_table_data(url,'FASTEST LAPS'):
        return None
    
    table_fastest_lap[0].rename(columns = {'Time of day':'Time_of_day', 'Avg Speed':'Avg_Speed'}, inplace = True)
    
    race_id = [race_num]*table_fastest_lap[0].shape[0]
    table_fastest_lap[0].insert(0, column = 'race_id', value = race_id)
    
    return table_fastest_lap[0][['race_id', 'Pos', 'Driver', 'Car', 'Lap', 'Time_of_day', 'Time', 'Avg_Speed']]

    
def get_qualifying_results(race_num, year):
    '''
    params: race_num, year
    
    returns the results of the qualifying fase before the race
    
    returns: name of the fase and a pandas dataframe ['race_id', 'Pos', 'Driver', 'Car', 'Q1', 'Q2', 'Q3', 'Laps']
    '''
    url = get_race_url(race_num, year)
    splitted_url = url.split('/')[:-1] + ['qualifying.html']
    url = '/'.join(splitted_url)
    
    try:
        table = pd.read_html(url)
    except ValueError:
        return None
    
    if not correct_table_data(url,'QUALIFYING'):
        return None
    
    table[0]['Driver'] = table[0]['Driver'].apply(first_2_words)
    
    race_id = [race_num]*table[0].shape[0]
    table[0].insert(0, column = 'race_id', value = race_id)
    
    return table[0][['race_id', 'Pos', 'Driver', 'Car', 'Q1', 'Q2', 'Q3', 'Laps']]


def race_has_sprint(race_num: int) -> bool:
    '''
    param: race_num
    
    returns true if a race has sprint stage
    
    return: Boolean
    
    '''
    web = get('http://ergast.com/api/f1/current')
    root = ET.XML(web.text)
    table = list(root)
    if table[0][race_num-1][5].tag.split('}')[1] == 'Qualifying':
        return True
    return False


def get_training_results(race_num, training_num, year):
    '''
    params: race_num, training_num (1, 2 or 3), year
    
    returns the results for a specific training practice before the race
    
    returns: pandas dataframe ['race_id', 'train_num', 'Pos', 'Driver', 'Car', 'Time', 'Gap', 'Laps']
    '''
    url = get_race_url(race_num, year)
    splitted_url = url.split('/')[:-1] + ['practice-'+str(training_num)+'.html']
    url = '/'.join(splitted_url)
    
    if training_num == 3 and race_has_sprint(race_num):
        return None
    
    try:
        table = pd.read_html(url)
    except ValueError:
        return None
    
    if not correct_table_data(url,'PRACTICE '+str(training_num)):
        return None
    
    table[0]['Driver'] = table[0]['Driver'].apply(first_2_words)
    
    race_id = [race_num]*table[0].shape[0]
    table[0].insert(0, column = 'race_id', value = race_id)
    
    train_num = [training_num]*table[0].shape[0]
    table[0].insert(1, column = 'train_num', value = train_num)
    
    return table[0][['race_id', 'train_num', 'Pos', 'Driver', 'Car', 'Time', 'Gap', 'Laps']]


def get_sprint_results(race_num, year):
    '''
    params: race_num, year
    
    if the race has an sprint returns the results of the sprint before the race
    
    returns: pandas dataframe ['race_id', 'Pos', 'Driver', 'Car', 'Laps', 'Time_Retired', 'PTS']
    '''
    url = get_race_url(race_num, year)
    
    if race_has_sprint(race_num):
        web = get(url)
        soup = BeautifulSoup(web.text, 'lxml')
        items = soup.find_all(class_='side-nav-item-link')
        url = 'https://www.formula1.com'+items[-5]['href']
        
        try:
            table = pd.read_html(url)
        except ValueError:
            return None
        
        if not correct_table_data(url,'SPRINT'):
            return None
        
        table[0]['Driver'] = table[0]['Driver'].apply(first_2_words)
        table[0].rename(columns = {'Time/Retired':'Time_Retired'}, inplace = True)
    
        race_id = [race_num]*table[0].shape[0]
        table[0].insert(0, column = 'race_id', value = race_id)
        
        return table[0][['race_id', 'Pos', 'Driver', 'Car', 'Laps', 'Time_Retired', 'PTS']]
    
    return None