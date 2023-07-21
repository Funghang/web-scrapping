import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, unquote

# Function to extract song details and lyrics
def extract_song_details(song_url, song_name):
    try:
        # Fetch the song page content
        response = requests.get(song_url)
        response.raise_for_status()

        # Handle redirection manually if necessary
        if response.status_code == 302:
            redirected_url = response.headers['Location']
            response = requests.get(redirected_url)

        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div containing the song lyrics
        song_lyrics_div = soup.find("div", class_="mainsong")

        if song_lyrics_div is None:
            print(f"No lyrics found for {song_name}")
            return

        # Extract the song lyrics
        song_lyrics = song_lyrics_div.get_text(separator="\n").strip()

        # Remove unwanted lines and empty lines
        cleaned_lyrics = [line.strip() for line in song_lyrics.split("\n") if line.strip() and not line.strip().startswith(("Your Name", "Your Email", "Receiver Name", "Receiver Email"))]

        # Join the cleaned lyrics
        cleaned_lyrics = "\n".join(cleaned_lyrics)

        # Find the song title
        song_title = soup.find("div", class_="song_profile").find("h1").text.strip()

        # Find the song profile details
        song_profile_div = soup.find("div", class_="song_profile")
        details = {label.text.strip(): value.text.strip() for label, value in zip(song_profile_div.find_all("strong"), song_profile_div.find_all("a"))}

        # Print the song details
        print(f"Song: {song_title}")
        print(f"Artist: {details.get('singer', 'Not available')}")
        print(f"Musician: {details.get('Musician', 'Not available')}")
        print(f"Lyricist: {details.get('Lyricist', 'Not available')}")
        print("Lyrics:")
        print(cleaned_lyrics)
        print("-------------------")
        print()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while retrieving details for {song_url}: {e}")


# Code to extract song names
base_url = "http://www.nepalisongchord.com/"

response = requests.get(base_url)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

# Find the artist details
links = soup.find("div", class_="songbookmenu").find_all("a")

# Counter for successfully extracted songs
total_songs_extracted = 0

# Iterate over the links
for link in links:
    link_url = link['href']
    if not link_url.endswith("#a") and link_url != "#":
        link_response = requests.get(link_url)
        link_response.raise_for_status()
        link_soup = BeautifulSoup(link_response.content, "html.parser")
        
        # Find the table with class "songlist" inside the link
        table = link_soup.find("table", class_="songlist")
        
        if table is None:
            print("Table not found.")
            continue
        
        # Find the links inside the table
        song_links = table.find_all("a")
         
        # Iterate over the song links and extract the song names
        for song_link in song_links:
            song_name = song_link.text.strip()
            encoded_song_name = quote(song_name.replace(" ", "_"))
            
            # Special cases where the song name in the URL is different
            song_name_mapping = {
                "Launani": "Launani_18thFret",
                "Sochnu dherai soche": "Sochun_dherai_soche",
                "Timi Bina": "Timi_Bina_Joheb",
                "Kun baato ma jaandai chau": "Kun_baat_ma_jaandai_chau_Nana_Band",
                "Samjhana": "Samjhana_Rory_and_Friends"
            }
            
            if song_name in song_name_mapping:
                encoded_song_name = quote(song_name_mapping[song_name].replace(" ", "_"))
                
            song_url = base_url + "song/" + encoded_song_name

            try:
                response = requests.get(song_url)
                response.raise_for_status()
                
                # Decode the song name from the URL
                decoded_song_name = unquote(song_url.split("/")[-1].replace("_", " "))

                # Call the function with the decoded song name
                extract_song_details(song_url, decoded_song_name)

                total_songs_extracted += 1
                
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while retrieving details for {song_url}: {e}")

# Print the total number of songs successfully extracted
print(f"Total songs successfully extracted: {total_songs_extracted}")
