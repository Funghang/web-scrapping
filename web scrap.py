import requests
from bs4 import BeautifulSoup
import json

url = "http://www.nepalisongchord.com/song/Maile_jaani_sake#a"
response = requests.get(url)
response.raise_for_status()
html_content = response.content

soup = BeautifulSoup(response.text, "html.parser")

# Find the song title
song_title = soup.find("div", class_="song_profile").find("h1").text.strip()

# Find the artist details
artist_details = soup.find("div", class_="song_profile").find_all("tr")

# Find the main song div for lyrics
main_song_div = soup.find("div", class_="mainsong")

# Extract the main song lyrics
main_lyrics = [line.strip() for line in main_song_div.get_text(separator="\n").split('\n') if line.strip()]

# Remove the last four lines
main_lyrics = main_lyrics[:-4]

# Process the artist details
details = {}
for detail in artist_details:
    key = detail.find("strong").text.strip()
    value = detail.find("td").text.strip().replace(":", "")
    details[key] = value

# Process the main lyrics and manage chord placement
formatted_lyrics = []
for line in main_lyrics:
    chords = line.split("\u00a0")
    formatted_line = " ".join(chords)
    formatted_lyrics.append(formatted_line)

# Create a dictionary for lyrics
song_details = {
    "title": song_title,
    "singer": details["Singer"],
    "musician": details["Musician"],
    "lyricist": details["Lyricist"],
    "lyrics": formatted_lyrics
}

# Convert the dictionary to JSON
output_json = json.dumps(song_details, indent=4)

# Print the JSON output
print(output_json)