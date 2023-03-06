import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR '
                  '3.5.30729)'}

url = 'https://www.liveresult.ru/football/Russia/Premier-League/scheduled'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
data = soup.find('div', class_='matches-list')


def parse_scheduled():
    # date = [date.text.split('\n')[1].strip() for date in
    #         data.find_all('div', class_='matches-list-date mt-3 d-flex align-items-center')]  пока хз что с датами делать
    time = (time.text.strip() for time in data.find_all(class_='match-time-time'))
    category = (category.text for category in data.find_all(class_='match-cat'))
    team1 = (team.text.strip() for team in data.find_all('span', class_='team team1'))
    team2 = (team.text.strip() for team in data.find_all('span', class_='team team2'))
    title = (f"{team[0]} - {team[1]}" for team in zip(team1, team2))
    score = (tire.text for tire in data.find_all(class_='score'))
    return list(zip(title, score, time, category))

# заполняем таблицу игрока на основе вкладки расписания. если счет появился, то в SQL таблицу апдейт счет.
