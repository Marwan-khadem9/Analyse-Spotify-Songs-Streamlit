import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd 
import os 

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

 
scope = 'user-library-read user-top-read'
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://localhost:5000',
        scope=scope
    )
)

st.set_page_config(page_title='Spotify Songs Analysis', page_icon=':musical_note:')
st.title('Analysis for your Top Songs')
st.write('Discover insights about your Spotify listening habits')

top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
track_ids = [track['id'] for track in top_tracks['items']]
audio_features = sp.audio_features(track_ids)

df = pd.DataFrame(audio_features)
df['track_name'] = [track['name'] for track in top_tracks['items']]
df = df[['track_name', 'danceability', 'energy', 'valence']]
df.set_index('track_name', inplace=True)

st.subheader('Audio Features for Top Tracks')
st.bar_chart(df, height=500)