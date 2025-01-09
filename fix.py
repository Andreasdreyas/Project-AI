import streamlit as st
import pandas as pd
import base64
import requests
import wikipedia
from datetime import datetime


# Set page configuration (perintah pertama)
st.set_page_config(
    page_title="Premier Insight",
    layout="wide",
    initial_sidebar_state="expanded"
)

light_mode_css = """
<style>
    body, .stApp {
        background-color: #FFFFFF; /* Warna putih untuk background */
        color: #000000; /* Warna hitam untuk teks */
    }

    h1, h2, h3, h4, h5, h6, p {
        color: #000000; /* Warna hitam untuk teks */
    }

    .block-container {
        background-color: #F8F9FA; /* Warna abu-abu terang untuk kontainer */
        border-radius: 8px; /* Membuat sudut kontainer sedikit melengkung */
        padding: 20px;
    }

    .stButton>button {
        background-color: #26DFF3; /* Warna biru untuk tombol */
        color: #000000 !important; /* Warna hitam untuk teks tombol */
        font-weight: bold; /* Membuat teks lebih tebal (opsional) */
        border-radius: 10px; /* Sudut membulat pada tombol */
        border: none; /* Menghapus border default */
        padding: 0px 6px; /* Ukuran padding lebih kecil */
        font-size: 2px; /* Ukuran font lebih kecil */
    }

    .stButton>button:hover {
        background-color: #0056b3; /* Warna biru lebih gelap saat hover */
        color: #000000 !important; /* Warna teks tetap hitam saat hover */
    }

    .stTextInput>div>div>input {
        color: #000000; /* Input teks menjadi hitam */
        background-color: #FFFFFF; /* Input background menjadi putih */
    }

    /* Styling khusus untuk select box */
    div[data-baseweb="select"] > div {
        background-color: #000000 !important; /* Latar belakang hitam */
        color: #FFFFFF !important; /* Teks putih */
        border-radius: 8px !important; /* Membuat sudut membulat */
    }

    div[data-baseweb="select"] .css-1nwi2ug-option {
        background-color: #000000 !important; /* Opsi dropdown hitam */
        color: #FFFFFF !important; /* Teks opsi dropdown putih */
    }

    div[data-baseweb="select"] .css-1nwi2ug-option:hover {
        background-color: #333333 !important; /* Efek hover abu-abu gelap */
    }

    div[data-baseweb="select"] > div > div {
        color: #FFFFFF !important; /* Teks di dalam dropdown putih */
    }
</style>
"""
st.markdown(light_mode_css, unsafe_allow_html=True)


# Fungsi untuk mengambil berita dari API
def fetch_news(query="Premier League"):
    API_KEY = "d54f31ab690946cd8f737d93a9005184" 
    URL = "https://newsapi.org/v2/everything"
    
    params = {
        "q": query,
        "apiKey": API_KEY,
        "sortBy": "publishedAt",
        "language": "en",
    }
    response = requests.get(URL, params=params)
    
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        
        # Filter berita hanya yang memiliki gambar dan mengandung "football" atau "soccer" dalam judul/deskripsi
        filtered_articles = [
            article for article in articles
            if article.get("urlToImage")  
        ]
        
        # Hapus duplikat berdasarkan judul
        unique_articles = {article['title']: article for article in filtered_articles}.values()
        
        return list(unique_articles)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# Fungsi untuk mengonversi gambar ke base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string
    


# Menu aplikasi
menu = ["Home", "Fixtures", "Club", "Players", "Injured Players", "Results", "Standings"]

# Menempatkan selectbox di tengah atas
with st.container():
    st.markdown("""
        <style>
            .centered-selectbox {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Membuat selectbox dengan gaya terpusat
    selected = st.selectbox(" ", menu, key="menu_select")




# Path gambar lokal
image_path = "bg judul.jpg"


# Menambahkan background image hanya pada title dan subtitle di semua halaman
try:
    encoded_image = image_to_base64(image_path)

    # Menambahkan CSS untuk background image
    st.markdown(
        f"""
        <style>
            .title {{
                background-image: url('data:image/jpg;base64,{encoded_image}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                padding: 40px;
                color: white;
                text-align: left;
                font-size: 48px;
                font-weight: bold;
            }}
            .subtitle {{
                background-image: url('data:image/jpg;base64,{encoded_image}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                padding: 20px;
                color: white;
                text-align: center;
                font-size: 24px;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0px;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            }}
        </style>
        """, 
        unsafe_allow_html=True
    )
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat gambar: {e}")

# Fungsi untuk mendapatkan URL logo berdasarkan nama tim
def get_team_standings_logo(team_name):
    club_logos = {
        'manchester united': "https://media.api-sports.io/football/teams/33.png",
        'chelsea': "https://media.api-sports.io/football/teams/49.png",
        'arsenal': "https://media.api-sports.io/football/teams/42.png",
        'liverpool': "https://media.api-sports.io/football/teams/40.png",
        'manchester city': "https://media.api-sports.io/football/teams/50.png",
        'tottenham hotspur': "https://media.api-sports.io/football/teams/47.png",
        'aston villa': "https://media.api-sports.io/football/teams/66.png",
        'brighton and hove albion': "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
        'fulham': "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg",
        'nottingham forest': "https://media.api-sports.io/football/teams/65.png",
        'bournemouth': "https://media.api-sports.io/football/teams/35.png",
        'brentford': "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
        'newcastle united': "https://media.api-sports.io/football/teams/34.png",
        'west ham united': "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
        'everton': "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
        'crystal palace': "https://media.api-sports.io/football/teams/52.png",
        'leicester city': "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
        'ipswich town': "https://media.api-sports.io/football/teams/57.png",
        'wolverhampton wanderers': "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
        'southampton': "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg"
    }
    return club_logos.get(team_name.lower(), "")



# Halaman Home
if selected == "Home":
    st.markdown('<div class="title"> Premier Insight</div>', unsafe_allow_html=True)
    
    # Fetch berita untuk halaman Home
    news_articles = fetch_news(query="Premier League football")
    if news_articles:
        cols = st.columns(2)  
        for idx, article in enumerate(news_articles[:6]):
            with cols[idx % 2]:  # Menampilkan berita di kolom
                st.markdown(
                    f"""
                    <div class="card">
                        <h4>{article['title']}</h4>
                        <p>{article['description'][:150]}...</p>
                        <img src="{article['urlToImage']}" style="width:100%; border-radius:10px;">
                        <p><small>Published: {datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").strftime('%d %B %Y')}</small></p>
                        <a href="{article['url']}" target="_blank"><button style="background-color:#6E5FF6; color:white; border:none; padding:8px 12px; border-radius:5px; cursor:pointer;">Baca Selengkapnya</button></a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("Tidak ada berita yang dapat ditampilkan. Periksa koneksi atau API Key Anda.")

    # Menampilkan match highlight dengan iframe tanpa judul
    st.subheader("Match Highlight")
    st.markdown("""
    <div style="overflow-x: scroll; white-space: nowrap; padding-bottom: 10px;">
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/hHRizp0kv6A" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/bgT4iMnmzzU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/g_r5mUrGqnw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/qcEaP6hMio4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
                <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/QRsFXm4vys0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/elcacalj8lI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/6HdeE4OJmI4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Menampilkan break down tactics dengan iframe tanpa judul
    st.subheader("Break Down Tactics")
    st.markdown("""
    <div style="overflow-x: scroll; white-space: nowrap; padding-bottom: 10px;">
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/XEC2L-sWyR4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/XZab_2A0X3c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/DiY9KpMiiQ8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/ygCmH-tmkMw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/eipq6Iej2is" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/6ES5MS9nu7c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        <div style="display: inline-block; width: 240px; margin-right: 20px;">
            <iframe width="240" height="135" src="https://www.youtube.com/embed/OQfCxt3k2Dg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown(
        """
        ---
        **Premier Insight** © 2024.
        """,
        unsafe_allow_html=True
    )

elif selected == "Fixtures":
    st.markdown('<div class="title"> Fixtures</div>', unsafe_allow_html=True)

elif selected == "Club":
    st.markdown('<div class="title"> Club</div>', unsafe_allow_html=True)

elif selected == "Players":
    st.markdown('<div class="title"> Players</div>', unsafe_allow_html=True)

elif selected == "Injured Players":
    st.markdown('<div class="title"> Injured Players</div>', unsafe_allow_html=True)

elif selected == "Results":
    st.markdown('<div class="title"> Results</div>', unsafe_allow_html=True)

elif selected == "Standings":
    st.markdown('<div class="title"> Standings</div>', unsafe_allow_html=True)


# Footer (opsional)
footer = """
<style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #777777;
        font-size: 12px;
    }
</style>
<div class="footer">
    Premier League Dashboard © 2024. All Rights Reserved.
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

# Fungsi untuk menentukan warna berdasarkan nama tim
def get_team_color(team_name):
    team_colors = {
        'manchester united': '#DA291C',  # Red
        'chelsea': '#034694',  # Blue
        'arsenal': '#EF0107',  # Red
        'liverpool': '#9E1B32',  # Red
        'manchester city': '#6CABDD',  # Light Blue
        'tottenham hotspur': '#132257',  # Biru
        'aston villa': '#6A2E84',  # Claret & Blue
        'brighton': '#005F87',  # Blue
        'fulham': '#000000',  # White and Black
        'nottingham forest': '#FF5F8C',  # Pink
        'bournemouth': '#D71A34',  # Red
        'brentford': '#F1B12D',  # Yellow & Red
        'newcastle': '#1E1E1E',  # Black and White
        'west ham': '#9E1B32',  # Claret & Blue
        'everton': '#003E6D',  # Blue
        'crystal palace': '#1B458F',  # Blue and Red
        'leicester': '#003090',  # Blue
        'ipswich': '#005AA7',  # Blue
        'wolves': '#FBB913',  # Gold & Black
        'southampton': '#D71920'  # Red
    }
    return team_colors.get(team_name.lower(), '#132257')  

# Fungsi untuk menentukan warna khusus untuk halaman Injured Players
def get_injured_team_color(team_name):
    injured_team_colors = {
        'manchester united': '#FF4500',  # Oranye
        'chelsea': '#4682B4',           # Steel Blue
        'arsenal': '#DC143C',           # Crimson
        'liverpool': '#8B0000',         # Dark Red
        'manchester city': '#87CEEB',   # Sky Blue
        'tottenham hotspur': '#6A5ACD', # Slate Blue
        'aston villa': '#9B0ACE',       # Dark Orchid
        'brighton & hove albion': '#0273BC',          # Cadet Blue
        'fulham': '#696969',            # Dim Gray
        'nottingham forest': '#FF1493', # Deep Pink
        'afc bournemouth': '#c23d3d',       # Tomato
        'brentford': '#CC2A1A',         # Gold
        'newcastle': '#808080',         # Gray
        'west ham united': '#800000',          # Maroon
        'everton': '#000080',           # Royal Blue
        'crystal palace': '#4169E1',    # Navy
        'leicester': '#0000FF',         # Blue
        'ipswich': '#1E90FF',           # Dodger Blue
        'wolverhampton wanderers': '#FFA500',            # Orange
        'southampton': '#CD5C5C'        # Indian Red
    }
    # Default warna jika tidak ditemukan
    return injured_team_colors.get(team_name.lower(), '#808080')  



# Fungsi untuk mendapatkan URL logo berdasarkan nama tim
def get_result_logo(team_name):
    club_logos = {
        'man utd': "https://media.api-sports.io/football/teams/33.png",
        'chelsea': "https://media.api-sports.io/football/teams/49.png",
        'arsenal': "https://media.api-sports.io/football/teams/42.png",
        'liverpool': "https://media.api-sports.io/football/teams/40.png",
        'man city': "https://media.api-sports.io/football/teams/50.png",
        'spurs': "https://media.api-sports.io/football/teams/47.png",
        'aston villa': "https://media.api-sports.io/football/teams/66.png",
        'brighton': "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
        'fulham': "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg",
        'nottingham forest': "https://media.api-sports.io/football/teams/65.png",
        'bournemouth': "https://media.api-sports.io/football/teams/35.png",
        'brentford': "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
        'newcastle': "https://media.api-sports.io/football/teams/34.png",
        'west ham': "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
        'everton': "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
        'crystal palace': "https://media.api-sports.io/football/teams/52.png",
        'leicester': "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
        'ipswich': "https://media.api-sports.io/football/teams/57.png",
        'wolves': "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
        'southampton': "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg"
    }
    return club_logos.get(team_name.lower(), "")



# Fungsi untuk mendapatkan URL logo berdasarkan nama tim
def get_team_injured_logo(team_name):
    club_logos = {
        'manchester united': "https://media.api-sports.io/football/teams/33.png",
        'chelsea': "https://media.api-sports.io/football/teams/49.png",
        'arsenal fc': "https://media.api-sports.io/football/teams/42.png",
        'liverpool fc': "https://media.api-sports.io/football/teams/40.png",
        'manchester city': "https://media.api-sports.io/football/teams/50.png",
        'tottenham hotspur': "https://media.api-sports.io/football/teams/47.png",
        'aston villa': "https://media.api-sports.io/football/teams/66.png",
        'brighton & hove albion': "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
        'fulham fc': "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg",
        'nottingham forest': "https://media.api-sports.io/football/teams/65.png",
        'afc bournemouth': "https://media.api-sports.io/football/teams/35.png",
        'brentford fc': "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
        'newcastle united': "https://media.api-sports.io/football/teams/34.png",
        'west ham united': "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
        'everton fc': "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
        'crystal palace': "https://media.api-sports.io/football/teams/52.png",
        'leicester': "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
        'ipswich town': "https://media.api-sports.io/football/teams/57.png",
        'wolverhampton wanderers': "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
        'southampton fc': "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg"
    }
    return club_logos.get(team_name.lower(), "")


# Membuat dictionary untuk memetakan nama tim yang ada di data ke nama tim yang benar
team_name_mapping = {
    "nott'm forest": "nottingham forest",
}

# Fungsi untuk mendapatkan URL logo berdasarkan nama tim
def get_team_player_logo(team_name):
    club_logos = {
        'man utd': "https://media.api-sports.io/football/teams/33.png",
        'chelsea': "https://media.api-sports.io/football/teams/49.png",
        'arsenal': "https://media.api-sports.io/football/teams/42.png",
        'liverpool': "https://media.api-sports.io/football/teams/40.png",
        'man city': "https://media.api-sports.io/football/teams/50.png",
        'spurs': "https://media.api-sports.io/football/teams/47.png",
        'aston villa': "https://media.api-sports.io/football/teams/66.png",
        'brighton': "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
        'fulham': "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg",
        'nottingham forest': "https://media.api-sports.io/football/teams/65.png",
        'bournemouth': "https://media.api-sports.io/football/teams/35.png",
        'brentford': "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
        'newcastle': "https://media.api-sports.io/football/teams/34.png",
        'west ham': "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
        'everton': "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
        'crystal palace': "https://media.api-sports.io/football/teams/52.png",
        'leicester': "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
        'ipswich': "https://media.api-sports.io/football/teams/57.png",
        'wolves': "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
        'southampton': "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg"
    }
    return club_logos.get(team_name.lower(), "")


# Fungsi untuk mendapatkan URL logo berdasarkan nama tim
def get_result_logo(team_name):
    club_logos = {
        'man united': "https://media.api-sports.io/football/teams/33.png",
        'chelsea': "https://media.api-sports.io/football/teams/49.png",
        'arsenal': "https://media.api-sports.io/football/teams/42.png",
        'liverpool': "https://media.api-sports.io/football/teams/40.png",
        'man city': "https://media.api-sports.io/football/teams/50.png",
        'tottenham': "https://media.api-sports.io/football/teams/47.png",
        'aston villa': "https://media.api-sports.io/football/teams/66.png",
        'brighton': "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
        'fulham': "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg",
        "nott'm forest": "https://media.api-sports.io/football/teams/65.png",
        'bournemouth': "https://media.api-sports.io/football/teams/35.png",
        'brentford': "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
        'newcastle': "https://media.api-sports.io/football/teams/34.png",
        'west ham': "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
        'everton': "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
        'crystal palace': "https://media.api-sports.io/football/teams/52.png",
        'leicester': "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
        'ipswich': "https://media.api-sports.io/football/teams/57.png",
        'wolves': "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
        'southampton': "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg"
    }
    return club_logos.get(team_name.lower(), "")



# Halaman Fixtures
if selected == "Fixtures":
    try:
        fixtures_file_path = "2024_premier_league_fixtures_df.csv"
        fixtures_df = pd.read_csv(fixtures_file_path)

        predictions_file_path = "output_final.csv"
        predictions_df = pd.read_csv(predictions_file_path, decimal=",")

        # Konversi kolom tanggal ke tipe datetime
        fixtures_df["Game Date"] = pd.to_datetime(fixtures_df["Game Date"])
        predictions_df["Game Date"] = pd.to_datetime(predictions_df["Game Date"])

        # Normalisasi nama tim
        fixtures_df["Home Team"] = fixtures_df["Home Team"].str.strip().str.lower()
        fixtures_df["Away Team"] = fixtures_df["Away Team"].str.strip().str.lower()
        predictions_df["Home Team"] = predictions_df["Home Team"].str.strip().str.lower()
        predictions_df["Away Team"] = predictions_df["Away Team"].str.strip().str.lower()

        # Menghilangkan tanda persen (%) dari kolom prediksi dan konversi ke float
        predictions_df["Home Win (%)"] = predictions_df["Home Win (%)"].str.rstrip('%').astype('float')
        predictions_df["Draw (%)"] = predictions_df["Draw (%)"].str.rstrip('%').astype('float')
        predictions_df["Away Win (%)"] = predictions_df["Away Win (%)"].str.rstrip('%').astype('float')

        # Filter untuk hanya menampilkan pertandingan hari ini atau yang akan datang
        today = pd.Timestamp.now().normalize()
        fixtures_df = fixtures_df[fixtures_df["Game Date"] >= today]

        # Menggabungkan data
        fixtures_df = fixtures_df.merge(predictions_df, on=["Game Date", "Home Team", "Away Team"], how="left")

        # Menambahkan kolom Match ID
        fixtures_df["Match ID"] = fixtures_df.apply(
            lambda x: f"{x['Game Date']}-{x['Home Team']}-{x['Away Team']}".replace(" ", "-").lower(), axis=1
        )

        for _, row in fixtures_df.iterrows():
            home_color = get_team_color(row['Home Team'])
            away_color = get_team_color(row['Away Team'])

            st.markdown(
                f"""
                <div style='background: white; 
                            padding: 15px; 
                            border-radius: 10px; 
                            margin-bottom: 20px;
                            border: 5px solid transparent;
                            border-image: linear-gradient(to right, {home_color}, {away_color}) 1;
                            color: black;'>
                    <h3 style='margin: 0; text-align: center;'>{row['Game Date'].strftime('%d %B %Y')}</h3>
                    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;'>
                        <div style='display: flex; align-items: center;'>
                            <img src='{row['Home Team Logo']}' width='50' style='margin-right: 10px;'>
                            <b>{row['Home Team'].title()}</b>
                        </div>
                        <div style='text-align: center; font-size: 24px;'><b>vs</b></div>
                        <div style='display: flex; align-items: center;'>
                            <b>{row['Away Team'].title()}</b>
                            <img src='{row['Away Team Logo']}' width='50' style='margin-left: 10px;'>
                        </div>
                    </div>
                    <p style='margin: 10px 0 0 0; text-align: center; font-size: 16px;'><b>Venue</b>: 🏟️ {row['Venue']}</p>
                </div>
                """, unsafe_allow_html=True
            )

            # Menampilkan prediksi jika tersedia
            if pd.notnull(row["Home Win (%)"]) and pd.notnull(row["Draw (%)"]) and pd.notnull(row["Away Win (%)"]):
                total_percentage = row['Home Win (%)'] + row['Draw (%)'] + row['Away Win (%)']
                draw_color = 'lightgray'  

                st.markdown(f"""
                <div style='display: flex; height: 20px; border-radius: 5px; overflow: hidden; margin-top: -10px;'>
                    <div style='background-color: {home_color}; width: {row['Home Win (%)'] / total_percentage * 100}%;'></div>
                    <div style='background-color: {draw_color}; width: {row['Draw (%)'] / total_percentage * 100}%;'></div>
                    <div style='background-color: {away_color}; width: {row['Away Win (%)'] / total_percentage * 100}%;'></div>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <div style='text-align: left; width: 30%;'>
                        <p><b>{row['Home Team'].title()}</b>: {row['Home Win (%)']:.2f}%</p>
                    </div>
                    <div style='text-align: center; width: 30%;'>
                        <p><b>Seri</b>: {row['Draw (%)']:.2f}%</p>
                    </div>
                    <div style='text-align: right; width: 30%;'>
                        <p><b>{row['Away Team'].title()}</b>: {row['Away Win (%)']:.2f}%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write("### Prediksi Pertandingan: Tidak tersedia")

            st.markdown("---")

    except FileNotFoundError as e:
        st.error(f"File tidak ditemukan: {e}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")


# Fungsi untuk mengambil ringkasan Wikipedia
def get_wikipedia_summary(club_name):
    try:
        page = wikipedia.page(f"{club_name} F.C.")
        return page.summary[:1000]  
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Terlalu banyak hasil untuk '{club_name} F.C.': {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Waktu habis saat mencoba mengakses Wikipedia."
    except wikipedia.exceptions.RedirectError:
        return f"Tautan untuk '{club_name} F.C.' mengarah ke halaman lain."
    except wikipedia.exceptions.PageError:
        return f"Informasi tidak tersedia di Wikipedia untuk '{club_name} F.C.'."
    except Exception as e:
        return f"Terjadi kesalahan: {e}"


# Halaman Club
if selected == "Club":
    try:
        fixtures_file_path = "2024_premier_league_fixtures_df.csv"
        predictions_file_path = "output_final.csv"

        fixtures_df = pd.read_csv(fixtures_file_path)
        predictions_df = pd.read_csv(predictions_file_path, decimal=",")

        # Konversi kolom tanggal ke tipe datetime
        fixtures_df["Game Date"] = pd.to_datetime(fixtures_df["Game Date"])
        predictions_df["Game Date"] = pd.to_datetime(predictions_df["Game Date"])

        # Normalisasi nama tim
        fixtures_df["Home Team"] = fixtures_df["Home Team"].str.strip().str.lower()
        fixtures_df["Away Team"] = fixtures_df["Away Team"].str.strip().str.lower()
        predictions_df["Home Team"] = predictions_df["Home Team"].str.strip().str.lower()
        predictions_df["Away Team"] = predictions_df["Away Team"].str.strip().str.lower()

        # Menghilangkan tanda persen (%) dari kolom prediksi dan konversi ke float
        predictions_df["Home Win (%)"] = predictions_df["Home Win (%)"].str.rstrip('%').astype(float)
        predictions_df["Draw (%)"] = predictions_df["Draw (%)"].str.rstrip('%').astype(float)
        predictions_df["Away Win (%)"] = predictions_df["Away Win (%)"].str.rstrip('%').astype(float)
        fixtures_df = fixtures_df.merge(predictions_df, on=["Game Date", "Home Team", "Away Team"], how="left")

        # Daftar klub dan logo mereka
        clubs = fixtures_df["Home Team"].unique()

        # Sorting daftar klub A-Z
        clubs = sorted(clubs)

        logos = {club: fixtures_df[fixtures_df["Home Team"] == club].iloc[0]["Home Team Logo"] for club in clubs}

        # State untuk menyimpan klub yang dipilih
        if 'selected_club' not in st.session_state:
            st.session_state.selected_club = None

        # Halaman utama (daftar klub)
        if st.session_state.selected_club is None:
            col1, col2, col3, col4 = st.columns(4)
            club_columns = [col1, col2, col3, col4]

            for i, club in enumerate(clubs):
                with club_columns[i % 4]:
                    if st.button(f"{club.title()}", key=f"club_{club}"):
                        st.session_state.selected_club = club
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center;">
                            <img src="{logos[club]}" style="width: 80px; height: 80px; object-fit: contain;">
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )

        # Halaman pertandingan klub
        else:
            club = st.session_state.selected_club

            # Menampilkan ringkasan Wikipedia
            summary = get_wikipedia_summary(club.title())
            st.write(summary)

            if st.button('Kembali ke Daftar Klub'):
                st.session_state.selected_club = None

            today = pd.Timestamp.now()
            club_fixtures = fixtures_df[(
                (fixtures_df["Home Team"] == club) | (fixtures_df["Away Team"] == club)) 
                & (fixtures_df["Game Date"] >= today)
            ]

            for _, row in club_fixtures.iterrows():
                home_color = get_team_color(row['Home Team'])
                away_color = get_team_color(row['Away Team'])

                st.markdown(
                    f"""
                    <div style='background: white; 
                                padding: 15px; 
                                border-radius: 10px; 
                                margin-bottom: 20px;
                                border: 5px solid transparent;
                                border-image: linear-gradient(to right, {home_color}, {away_color}) 1;
                                color: black;'>
                        <h3 style='margin: 0; text-align: center;'>{row['Game Date'].strftime('%d %B %Y')}</h3>
                        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;'>
                            <div style='display: flex; align-items: center;'>
                                <img src='{row['Home Team Logo']}' width='50' style='margin-right: 10px;'>
                                <b>{row['Home Team'].title()}</b>
                            </div>
                            <div style='text-align: center; font-size: 24px;'><b>vs</b></div>
                            <div style='display: flex; align-items: center;'>
                                <b>{row['Away Team'].title()}</b>
                                <img src='{row['Away Team Logo']}' width='50' style='margin-left: 10px;'>
                            </div>
                        </div>
                        <p style='margin: 10px 0 0 0; text-align: center; font-size: 16px;'><b>Venue</b>: 🏟️ {row['Venue']}</p>
                    </div>
                    """, unsafe_allow_html=True
                )


                # Menampilkan prediksi jika tersedia
                if pd.notnull(row["Home Win (%)"]) and pd.notnull(row["Draw (%)"]) and pd.notnull(row["Away Win (%)"]):
                    st.write("### Prediksi Menang: ")
                    total_percentage = row['Home Win (%)'] + row['Draw (%)'] + row['Away Win (%)']
                    home_color = get_team_color(row['Home Team'])
                    away_color = get_team_color(row['Away Team'])
                    draw_color = '#FFFFFF'

                    st.markdown(f"""
                    <div style='display: flex; height: 30px; margin-bottom: 10px; border: 1px solid #ddd;'>
                        <div style='background-color: {home_color}; width: {(row['Home Win (%)'] / total_percentage) * 100}%;'></div>
                        <div style='background-color: {draw_color}; width: {(row['Draw (%)'] / total_percentage) * 100}%;'></div>
                        <div style='background-color: {away_color}; width: {(row['Away Win (%)'] / total_percentage) * 100}%;'></div>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <div style='text-align: left; width: 30%;'><b>{row['Home Team'].title()}</b>: {row['Home Win (%)']:.2f}%</div>
                        <div style='text-align: center; width: 30%;'><b>Seri</b>: {row['Draw (%)']:.2f}%</div>
                        <div style='text-align: right; width: 30%;'><b>{row['Away Team'].title()}</b>: {row['Away Win (%)']:.2f}%</div>
                    </div>
                    <hr style='border: 1px solid #ccc; margin: 10px 0;' />
                    """, unsafe_allow_html=True)
                else:
                    st.write("### Prediksi Pertandingan: Tidak tersedia")

                st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(f"File '{fixtures_file_path}' tidak ditemukan. Pastikan file ada di lokasi yang benar.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")


# Halaman Players
elif selected == "Players":
    col1, col2 = st.columns([4, 1]) 
    
    with col2:
        search_query = st.text_input("Search Players", "", placeholder="Search for a Player")

    st.markdown("""
        <style>
            /* Styling container selectbox */
            div[role="combobox"] {
                background-color: white !important; /* Background putih */
                color: black !important; /* Teks hitam */
                border-radius: 8px !important; /* Border radius */
                border: 1px solid #ccc !important; /* Border abu-abu */
            }

            /* Styling opsi dropdown */
            div[role="listbox"] {
                background-color: white !important; /* Background putih */
                color: black !important; /* Teks hitam */
            }

            /* Styling saat opsi di-hover */
            div[role="option"]:hover {
                background-color:rgb(74, 165, 204) !important; /* Background hover abu-abu */
                color: black !important; /* Teks hitam */
            }
        </style>
    """, unsafe_allow_html=True)

    try:
        file_path = "cleaned_merged_gw.csv"
        players_df = pd.read_csv(file_path)

        # Menyaring kolom yang relevan
        players_df = players_df[[ 
            "name", "team", "position", "goals_scored", "assists", 
            "yellow_cards", "red_cards"
        ]]

        # Mengganti nama kolom agar lebih rapi untuk tampilan
        players_df.columns = [
            "Player Name", "Team", "Position", "Goals Scored", "Assists", 
            "Yellow Cards", "Red Cards"
        ]

        # Filter berdasarkan query pencarian
        if search_query:
            players_df = players_df[players_df['Player Name'].str.contains(search_query, case=False, na=False)]

        col1, col2 = st.columns(2)

        with col1:
            clubs = players_df["Team"].unique()
            selected_club = st.selectbox(
                "Filter by Club", 
                options=["All"] + list(clubs),
                key="club_filter"
            )
            if selected_club != "All":
                players_df = players_df[players_df["Team"] == selected_club]

        with col2:
            positions = players_df["Position"].unique()
            selected_position = st.selectbox(
                "Filter by Position", 
                options=["All"] + list(positions),
                key="position_filter"
            )
            if selected_position != "All":
                players_df = players_df[players_df["Position"] == selected_position]

        # Menambahkan logo klub ke kolom "Team"
        players_df["Team"] = players_df["Team"].apply(lambda team: f'<img src="{get_team_player_logo(team)}" width="30" height="30" style="margin-right: 10px; object-fit: contain;"> {team}')

        # Menampilkan tabel pemain dengan logo klub
        st.write(
            players_df.to_html(index=False, escape=False, justify='center'), 
            unsafe_allow_html=True
        )

    except FileNotFoundError:
        st.error(f"File '{file_path}' tidak ditemukan. Pastikan file ada di lokasi yang benar.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")


# Halaman Injured Players
elif selected == "Injured Players":
    try:
        file_path = "injured.csv"
        injured_df = pd.read_csv(file_path)

        # Normalisasi nama klub
        injured_df["Club"] = injured_df["Club"].str.lower().str.strip()
        clubs = injured_df["Club"].unique()

        for club in clubs:
            team_color = get_injured_team_color(club)
            logo_url = get_team_injured_logo(club)
            club_display_name = club.title()

            st.markdown(
                f"""
                <div style="
                    background-color: {team_color};
                    border-radius: 10px;
                    padding: 10px;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                    color: #FFFFFF;
                    font-size: 20px;
                    justify-content: space-between;
                ">
                    <div style="display: flex; align-items: center;">
                        <div style="display: flex; justify-content: center;">
                            <img src="{logo_url}" style="width: 50px; height: 50px; object-fit: contain;">
                        </div>
                        <strong style="margin-left: 10px;">{club_display_name}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Filter data pemain cedera berdasarkan klub
            club_injuries_df = injured_df[injured_df["Club"] == club]

            # Menampilkan tabel menggunakan HTML dengan styling
            table_html = club_injuries_df[["Player", "Injury", "Until"]].to_html(index=False, escape=False)
            st.markdown(
                f"""
                <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;  /* Mengatur semua kolom ke kiri */
                }}
                th {{
                    background-color: #f2f2f2;
                    color: #333;
                }}
                td {{
                    color: #333;
                }}
                td, th {{
                    text-align: left !important; /* Pastikan kolom Player, Injury, Until berada di kiri */
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="overflow-x:auto;">
                    {table_html}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<hr>", unsafe_allow_html=True)

    except FileNotFoundError:
        st.error(f"File '{file_path}' tidak ditemukan.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")





# Halaman Results
elif selected == "Results":
    try:
        results_file_path = "Result_Baruu.csv"
        results_df = pd.read_csv(results_file_path, sep=',')  
        results_df["Game Date"] = pd.to_datetime(results_df["Game Date"], dayfirst=True)

        # Filter untuk menampilkan hasil pertandingan hingga tanggal hari ini
        today = pd.Timestamp.now()
        results_df = results_df[results_df["Game Date"] <= today]

        # Urutkan berdasarkan tanggal terbaru di bagian atas
        results_df = results_df.sort_values(by="Game Date", ascending=False)

        for _, row in results_df.iterrows():
            home_color = get_team_color(row['Home Team'])
            away_color = get_team_color(row['Away Team'])

            # Gunakan fungsi get_team_player_logo untuk mengambil URL logo
            home_logo = get_result_logo(row["Home Team"])
            away_logo = get_result_logo(row["Away Team"])

            st.markdown(f"""
            <div style='
                text-align: center; 
                margin: 20px auto; 
                padding: 15px; 
                border: 5px solid transparent; 
                border-radius: 10px; 
                background-color: #FFFFFF; 
                color: #000000; 
                font-size: 16px; 
                font-weight: none; 
                border-image: linear-gradient(to right, {home_color}, {away_color}) 1;
            '>
                <div style='margin-bottom: 10px;'>
                    <span style='font-size: 30px; font-weight: 500;'>{row['Game Date'].strftime('%d %B %Y')}</span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div style='text-align: center; flex: 1;'>
                        <img src='{home_logo}' width='60'>
                        <p style='font-weight: bold;'>{row["Home Team"].title()}</p>
                    </div>
                    <div style='text-align: center; flex: 1; font-size: 35px; font-weight: bold;'>
                        {row['Skor Home Team']} - {row['Skor Away Team']}
                    </div>
                    <div style='text-align: center; flex: 1;'>
                        <img src='{away_logo}' width='60'>
                        <p style='font-weight: bold;'>{row["Away Team"].title()}</p>
                    </div>
                </div>
                <div style='margin-top: 10px; text-align: center; font-size: 16px; color: rgb(0, 0, 0);'>
                    <b>Venue:</b> 🏟️ {row['Venue']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("---")

    except FileNotFoundError as e:
        st.error(f"File tidak ditemukan: {e}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")



# Halaman Standings
elif selected == "Standings":
    try:
        file_path = "premier_league_table.csv"
        standings_df = pd.read_csv(file_path)

        html_table = """
        <style>
            .standings-container {
                width: 100%;
                font-family: Arial, sans-serif;
            }
            .row {
                display: flex;
                align-items: center;
                padding: 8px 0;
                border-bottom: 1px solid #ddd;
            }
            .ucl-zone {
                border-left: 8px solid #007bff; /* Biru untuk UCL */
            }
            .uel-zone {
                border-left: 8px solid #ff7f00; /* Oranye untuk UEL */
            }
            .uecl-zone {
                border-left: 8px solid #28a745; /* Hijau untuk UECL */
            }
            .degradation {
                border-left: 8px solid #dc3545; /* Merah untuk degradasi */
            }
            .default-zone {
                border-left: 8px solid transparent; /* Baris tanpa warna */
            }
            .row-content {
                display: flex;
                justify-content: space-between;
                width: 100%;
                padding-left: 10px; /* Spasi setelah garis warna */
            }
            .team {
                display: flex;
                align-items: center;
            }
            .team img {
                margin-right: 10px;
                width: 30px;
                height: 30px;
            }
            .header {
                font-weight: bold;
                padding: 8px 0;
                border-bottom: 2px solid #000;
            }
            .points {
                font-weight: bold;
                color: #000;
            }
            .arrow-up {
                color: #28a745; /* Hijau */
                font-weight: bold;
            }
            .arrow-down {
                color: #dc3545; /* Merah */
                font-weight: bold;
            }
            .arrow-stay {
                color: #000; /* Hitam */
                font-weight: bold;
            }
        </style>
        <div class="standings-container">
            <div class="row header">
                <div style="width: 5%; text-align: center;">Position</div>
                <div style="width: 5%; text-align: center;"></div> <!-- Kolom Change kosong -->
                <div style="width: 35%; text-align: left;">Club</div>
                <div style="width: 10%; text-align: center;">Played</div>
                <div style="width: 10%; text-align: center;">Won</div>
                <div style="width: 10%; text-align: center;">Drawn</div>
                <div style="width: 10%; text-align: center;">Lost</div>
                <div style="width: 10%; text-align: center;">GD</div>
                <div style="width: 10%; text-align: center;" class="points">Points</div>
            </div>
        """

        # Iterasi untuk menambahkan baris tim sesuai posisi
        total_teams = len(standings_df)
        for _, row in standings_df.iterrows():
            position = row['Position']
            if position <= 4:  # Zona UCL
                zone_class = "ucl-zone"
            elif position <= 6:  # Zona UEL
                zone_class = "uel-zone"
            elif position == 7:  # Zona UECL
                zone_class = "uecl-zone"
            elif position > total_teams - 3:  # Zona Degradasi
                zone_class = "degradation"
            else:
                zone_class = "default-zone"  # Baris tanpa warna di samping kiri

            team_logo = get_team_standings_logo(row['Club'])


            html_table += f"""
            <div class="row {zone_class}">
                <div class="row-content">
                    <div style="width: 5%; text-align: center;">{row['Position']}</div>
                    <div style="width: 35%; text-align: left;" class="team">
                        <img src="{team_logo}" alt="Logo">
                        {row['Club']}
                    </div>
                    <div style="width: 10%; text-align: center;">{row['Played']}</div>
                    <div style="width: 10%; text-align: center;">{row['Won']}</div>
                    <div style="width: 10%; text-align: center;">{row['Drawn']}</div>
                    <div style="width: 10%; text-align: center;">{row['Lost']}</div>
                    <div style="width: 10%; text-align: center;">{row['GD']}</div>
                    <div style="width: 10%; text-align: center;" class="points">{row['Points']}</div>
                </div>
            </div>
            """

        html_table += "</div>"
        st.components.v1.html(html_table, height=600, scrolling=True)

    except FileNotFoundError:
        st.error(f"File '{file_path}' tidak ditemukan. Pastikan file ada di lokasi yang benar.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
