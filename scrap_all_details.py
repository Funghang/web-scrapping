##extracts the song details from www.nepalisongchord.com 
import requests
from bs4 import BeautifulSoup

url_base = "http://www.nepalisongchord.com/song/"
song_names = ["Launani_18thFret", "Mayalu_le", "Mildaina_Kathaharu", "Tyo_raatko", "Eklo_chhu", "NepaliFullTab", "Hidda_Hiddai",
              "PINJADA_KO_SUGA", "Gurasai_fulyo", "Nepali", "Kahile_Kahile", "Chaubandi_Choli", "Mutu_Bhari_Bhari",
              "Sambodhan_timilai_gardaichu", "Timilai_Piratile_bandhula", "(1974_AD)Deurali_Bhanjyang", "Chundaina_Timro_Mayale",
              "Parelima_lukai_rakhana", "Dherai_dherai_aauncha_manama", "Malai_bhanna_aaundaina", "Timi_aauna", "Ek_Mauka",
              "Birsana_Sakina", "Yaad_nadeo", "Harpal", "Aatma", "Sapana_Ra_Kartavya", "Jaba_timi_hunchau", "Nasamjha_bhulidinelai",
              "Aaja_:_Aaja_Samjhi_Lyaunda", "Kaash_mera", "Navana_mero_maya", "Aaja", "SisireJhari", "SaraKhusi", "Farki_Farki",
              "when_i_am_alone", "Rato_ra_Chandra_Surya", "Hoinau_Meri_Hoinau", "Joon_Chamiki_Rahecha", "Joonsukai_baadala_ma",
              "Maile_jaani_sake", "Aakashma_lekhe", "Priyatma", "Arkakai", "Dina_Katchu", "Chahidaina_satai_juni",
              "Will_You_Marry_Me", "Ma_maya_garchu", "Pari", "Prem_patra", "I_love_you", "Dubna_deu", "Sakchauvane_Visha_Deu",
              "Dakschinkali_jaanda_(Kanchi)", "Samjhera_malai", "Sukha_ra_dukha", "Din", "Hida_timi_aaphnai_baato", "Ye_dautari",
              "Yo_man_ko_k_bhar_huncha", "Sanjha_ko_jun_sangai", "Ankha_ko_nid_koshi_laane", "Jati_Maya_Laye_Pani",
              "Katai_tada_timi_bata", "Rituharuma_Timi", "Udi_Jaun_Bhane", "E_kancha_malai_sunko_tara", "Eklai_Basda",
              "Hera_na_hera_kaancha", "Aundai_chu_ma_dherai", "Euta_Chittiko_sahara_le", "Lukna_deu_malai",
              "Praya_sadhain_ma", "Chiya_baarima", "E_Mori_kali_na_gori", "Time_pheri_aauna", "Adhuro_Prem",
              "Ho_timi_nai_chahe", "Mohani_layo", "Gayo_Gayo_Jawani_Gayo", "Chahanchu_ma", "Jhari_Pareko_din",
              "Bolau_Bhane_Timilai", "Maya_meri_sanjha_bani", "Hajar_ankha_herne", "Mutu_Jali_Rahecha","Jaha_chan_buddhaka_ankha",
              "Jati_chot_dinchau_deu", "Achaanak", "Oh_Riya", "Maya_laauna_ta","Bihani_ko_mirmire", "Tadpinchu", "Mann", "Timro_maya",
              "Ke_Samjhi_Khelyou", "Aaja_aakashma_euta_tara", "Man_chade_maichyang_lai", "Hiun_bhanda_chiso","Suna_katha_euta_geet",
              "Manko_kura_lai", "Ratkorani", "Samaya_Panchi_ho", "Chiso_chiso_hawama", "Ma_ta_door_dekhi_aayen", "Kasto_Rahecha_Jeevan_mero",
              "Ma_pathar_ko_devata_hoina", "Mero_aankhama_hardam", "Adharko_Muskan_ta_kehi_hoina", "Timi_Aakasko_Joon_bhayou", "Dinko_Ujyaloma_Lukai_Rakchu", "Hnu_yatri_euta",
              "Kati_kamjor_rahecha", "Biteka_kura", "Farkera_aaune_chaina", "Priye_timi_ayou", "Oh_Amira", "Nadhukeko_man", "Mayako_dorile(_Ju_Ju_Na_Na_)", "Kali_kali_hissi_pareki",
              "Andhyaroma_chaaunchau_timi", "Timi_samu_nabhayer", "Timi_Sanga_Dungama", "Safal_timro_tyo_jindagilai", "Baiguni_chau_bhanau_bhane", "Yestai_nai_cha_yahanko_reet",
              "Paniko_rimjhim_barsat_ko_bela", "Malai_nazarko_isara_nadeu", "Timro_Ikchyama_ma_hansi_dinchu", "Hijo_Samma_Eklo_thiyen",
              "Awaz_deu", "Tara_matra_hoina_timilai", "Ghumti_ma_naau_hai", "Rajamati_Kumati", "Resam_firiri", "MalShree_dhun", "Aanshu_jhardina",
              "Kun_baato_ma_jaandai_chau", "Saune_Jharima", "Shanti_lukau_kahan", "Mutu_mero_chudi_lagin", "Samhali_rakhe_yo_man", "Tyo_pari_dandaima",
              "Chari_udyo_baadal_chuna_lai", "Memories", "Ke_bhanne_hamro_samaya", "Tunguna_ko_dhunma", "Rastriya_Gaan", "Bidesh_Jane_Mayalu", "Malai_Maaf_gari_deu",
              "SADHAI_MA", "Pahilo_Maya", "Thakeko_e_nayan_ma"]

# Iterate over each song name
for song_name in song_names:
    song_url = url_base + song_name

    try:
        # Fetch the song page content
        response = requests.get(song_url)
        response.raise_for_status()

        # Handle redirection manually if necessary
        if response.status_code == 302:
            redirected_url = response.headers['Location']
            response = requests.get(redirected_url)

        html_content = response.content

        soup = BeautifulSoup(html_content, "html.parser")

        # Find the div containing the song lyrics
        song_lyrics_div = soup.find("div", class_="mainsong")

        if song_lyrics_div is None:
            print(f"No lyrics found for {song_name}")
            continue

        # Extract the song lyrics
        song_lyrics = song_lyrics_div.get_text(separator="\n").strip()

        # Remove unwanted lines and empty lines
        lines = song_lyrics.split("\n")
        cleaned_lyrics = []
        for line in lines:
            if not line.strip().startswith(("Your Name", "Your Email", "Receiver Name", "Receiver Email")) and line.strip() != "":
                cleaned_lyrics.append(line)

        # Join the cleaned lyrics
        cleaned_lyrics = "\n".join(cleaned_lyrics)

        # Find the song title
        song_title = soup.find("div", class_="song_profile").find("h1").text.strip()

        # Find the song profile details
        song_profile_div = soup.find("div", class_="song_profile")
        labels = song_profile_div.find_all("strong")
        values = song_profile_div.find_all("a")

        # Extract the artist details
        details = {}
        for label, value in zip(labels, values):
            label_text = label.text.strip()
            value_text = value.text.strip()
            if label_text.lower() in ['singer', 'band']:
                details['Artist'] = value_text
            else:
                details[label_text] = value_text

        # Print the song details
        print(f"Song: {song_title}")
        if 'Artist' in details:
            print(f"Artist: {details['Artist']}")
        else:
            print("Artist: Not available")
        if 'Musician' in details:
            print(f"Musician: {details['Musician']}")
        else:
            print("Musician: Not available")
        if 'Lyricist' in details:
            print(f"Lyricist: {details['Lyricist']}")
        else:
            print("Lyricist: Not available")
        print("Lyrics:")
        print(cleaned_lyrics)
        print("-------------------")
        print()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while retrieving details for {song_name}: {e}")