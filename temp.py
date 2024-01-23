from bs4 import BeautifulSoup
import requests
import splash
from playwright.sync import sync_playwright

def scrap_yt(song_name):
    try:
        # scrap the youtube for the song
        # return the link of the song
        # if the song is not found return None
        # else return the link
        url = "https://www.youtube.com/results?search_query=" + song_name
        response = requests.get(url)
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        video_link = soup.find("a", {"class": "class=style-scope ytd-video-renderer > text-wrapper style-scope ytd-video-renderer > style-scope ytd-video-renderer > title-and-badge style-scope ytd-video-renderer"})["href"]
        print(video_link)
        embedded_link = f"https://www.youtube.com/embed{video_link}"
        return embedded_link
    except Exception as e:
        print(e)
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
# scrap_yt("hey")

song_name="test"
url = "https://www.youtube.com/results?search_query=" + song_name
response = splash.get(url)
print(response)