# First install beautifulsoap4 using : pip install beautifulsoup4
# Second install requests_html5 using : pip install requests-html

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests_html import HTMLSession
import requests
import time

# Debug variable (for console text)
DEBUG = True


# Timeout Function
def timeout():
    print('retrying in ...')
    for _ in range(5, -1, -1):
        time.sleep(1)
        print(_)


# Function to web scrapper player's age
def scrap_age(id, name, total, count):
    url = f'https://www.hltv.org/player/{id}/{name}'
    session = HTMLSession()

    resp = session.get(url)
    resp.html.render()
    html = resp.html.html

    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find_all("span", {'class': "profile-player-stat-value"})
    if span and span[0].text.split()[0].isdigit():
        # print(span[0].text.split()[0])
        total += 1
        return span[0].text.split()[0], total, count

    else:
        div = soup.find_all("div", {'class': "listRight"})

        if div and div[1].text.split()[0].isdigit():
            # print(div[1].text.split()[0])
            total += 1
            return div[1].text.split()[0], total, count

        else:
            count += 1
            total += 1
            # print('-')
            return '-', total, count


# Function to web scrapper event's tier
def scrap_lan(event_id):
    url = f'https://www.hltv.org/results?event={event_id}&matchType=Online'

    ua = UserAgent()
    header = {
        "User-Agent": ua.random
    }
    resp = requests.get(url, headers=header, sleep=1)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup
    # div_result = soup.find_all("div", {'class': "result-con"})
    #
    # if div_result:
    #     i_stars = soup.find_all("i", {'class': "fa fa-star star"})
    #     total_stars = len(div_result) * 5
    #     current_stars = len(i_stars)
    #     avg_stars = current_stars / total_stars
    #     for div in div_result:
    #         # Find href and Extract match_id
    #         href = div.find('a', href=True)
    #         url = href['href']
    #         match_id = url.split('/', 3)
    #         # Find and Extract Stars from Match
    #         stars = div.find_all("i", {'class': "fa fa-star star"})
    #     return match_id[2], len(stars), 0, f'{avg_stars:.3f}'
    #
    # else:
    #     url = f'https://www.hltv.org/results?event={event_id}&matchType=Lan'
    #     session = HTMLSession()
    #
    #     resp = session.get(url, headers=header)
    #     resp.html.render(timeout=20)
    #     html = resp.html.html
    #     session.close()
    #
    #     soup = BeautifulSoup(html, 'html.parser')
    #     div_result = soup.find_all("div", {'class': "result-con"})
    #     i_stars = soup.find_all("i", {'class': "fa fa-star star"})
    #
    #     total_stars = len(div_result) * 5
    #     current_stars = len(i_stars)
    #     avg_stars = current_stars / total_stars
    #
    #     for div in div_result:
    #         # Find href and Extract match_id
    #         href = div.find('a', href=True)
    #         url = href['href']
    #         match_id = url.split('/', 3)
    #         # Find and Extract Stars from Match
    #         stars = div.find_all("i", {'class': "fa fa-star star"})
    #     return match_id[2], len(stars), 1, f'{avg_stars:.3f}'


def scrap_all(event_id):
    url = f'https://www.hltv.org/results?event={event_id}&matchType=Online'
    session = HTMLSession()

    ua = UserAgent()
    header = {
        "User-Agent": ua.random
    }
    resp = session.get(url, headers=header)
    resp.html.render(timeout=20)
    html = resp.html.html
    session.close()

    soup = BeautifulSoup(html, 'html.parser')
    div_result = soup.find_all("div", {'class': "result-con"})

    if div_result:
        i_stars = soup.find_all("i", {'class': "fa fa-star star"})
        total_stars = len(div_result) * 5
        current_stars = len(i_stars)
        avg_stars = current_stars / total_stars
        for div in div_result:
            # Find href and Extract match_id
            href = div.find('a', href=True)
            url = href['href']
            match_id = url.split('/', 3)
            # Find and Extract Stars from Match
            stars = div.find_all("i", {'class': "fa fa-star star"})
        return match_id[2], len(stars), 0, f'{avg_stars:.3f}'

    else:
        url = f'https://www.hltv.org/results?event={event_id}&matchType=Lan'
        session = HTMLSession()

        resp = session.get(url, headers=header)
        resp.html.render(timeout=20)
        html = resp.html.html
        session.close()

        soup = BeautifulSoup(html, 'html.parser')
        div_result = soup.find_all("div", {'class': "result-con"})
        i_stars = soup.find_all("i", {'class': "fa fa-star star"})

        total_stars = len(div_result) * 5
        current_stars = len(i_stars)
        avg_stars = current_stars / total_stars

        for div in div_result:
            # Find href and Extract match_id
            href = div.find('a', href=True)
            url = href['href']
            match_id = url.split('/', 3)
            # Find and Extract Stars from Match
            stars = div.find_all("i", {'class': "fa fa-star star"})
        return match_id[2], len(stars), 1, f'{avg_stars:.3f}'

