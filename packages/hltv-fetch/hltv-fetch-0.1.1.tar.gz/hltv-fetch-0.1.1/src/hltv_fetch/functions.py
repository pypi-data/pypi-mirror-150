from bs4 import BeautifulSoup
import requests
from datetime import datetime


def get_live_matches():
    response = []
    url = 'https://www.hltv.org/matches'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    live_matches = soup.find("div", class_="liveMatchesContainer").find_all("div", class_="liveMatch-container")

    
    for match in live_matches:
        match_link = "https://www.hltv.org" + match.find("a", class_="match")["href"]
        match_info = create_match_dictionary(match_link)
        response.append(match_info)

    return response


def get_future_matches(date): # dd.mm.yyyy
    try:
        actual_datetime = datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        print("Please, use correct date format (dd.mm.yyyy)")
    else:
        response = []
        url = 'https://www.hltv.org/matches'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        upcoming_matches_containers = soup.find("div", class_="upcomingMatchesAll").find_all("div", class_="upcomingMatchesSection")

        for upcoming_matches_container in upcoming_matches_containers:
            games_date_str = upcoming_matches_container.find("span", class_="matchDayHeadline").get_text().split('-', 1)[1].strip()
            games_datetime = datetime.strptime(games_date_str, "%Y-%m-%d")
            if games_datetime == actual_datetime:
                matches = upcoming_matches_container.find_all("div", class_="upcomingMatch")
                for match in matches:
                    link = 'https://www.hltv.org' + match.find("a")['href']
                    match_info = create_match_dictionary(link)
                    response.append(match_info)
            else:
                next
        return response
        

def create_match_dictionary(match_link):
    r = requests.get(match_link)
    soup = BeautifulSoup(r.text, "lxml")

    match_info = {}

    #finding match box (there is some useful info there)
    match_box = soup.find("div", class_="teamsBox")
    
    #adding event details to match info
    event_details = {}
    event_name = match_box.find("div", class_="event").get_text()
    # event_time = match_box.find("div", class_="time").get_text()
    # event_date = match_box.find("div", class_="date").get_text()
    event_link = "https://www.hltv.org" + match_box.find("div", class_="event").find("a")["href"]
    event_id = event_link[28:].split('/', 1)[0]

    event_details["id"] = event_id
    event_details["name"] = event_name
    # event_details["time"] = event_time
    # event_details["date"] = event_date Probably should do another func for all these
    event_details["link"] = event_link

    match_info["event"] = event_details

    #adding teams details to the match info
    teams = match_box.find_all("div", class_="team")
    for idx, team in enumerate(teams):
        team_details = {}
        team_name = team.find("div", class_="teamName").get_text()
        team_link = "https://www.hltv.org" + team.find("a")["href"]
        team_id = team_link[26:].split('/', 1)[0]

        team_details['id'] = team_id
        team_details["team"] = team_name
        team_details["link"] = team_link
        match_info["team" + str(idx + 1)] = team_details
    
    match_info["link"] = match_link

    return match_info
