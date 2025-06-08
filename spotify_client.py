# Author: Farouk Balogun

import json
import os
import spotipy
import time
from spotipy.cache_handler import CacheHandler
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "")
SPOTIFY_SCOPES = os.getenv("SPOTIFY_SCOPES", "")
SPOTIFY_TOKEN_INFO = os.getenv("SPOTIFY_TOKEN_INFO", "")


class CustomLocalCacheHandler(CacheHandler):
    """
    A custom CacheHandler that stores and retrieves token info from an environment variable.
    """

    def __init__(self, local_token_info_str: str):
        # Parse the initial token info from the local token info string.
        self.token_info = (
            json.loads(local_token_info_str) if local_token_info_str else None
        )
        if not self.token_info:
            print("No initial token found in environment variable.")

    def get_cached_token(self):
        """
        Retrieves the cached token information.
        """
        if self.token_info and self.token_info.get("expires_at", 0) > int(time.time()):
            # If we have a token and it's not expired, return it
            return self.token_info
        elif self.token_info and self.token_info.get("refresh_token"):
            # If token is expired but we have a refresh token, Spotipy's auth_manager
            # will use the refresh_token to get a new access token internally.
            # We just need to ensure the refresh_token is available.
            return self.token_info
        else:
            print("No valid token or refresh token found in cache handler.")
            return None

    def save_token_to_cache(self, token_info):
        """
        Saves the new or refreshed token information.
        """
        self.token_info = token_info


class SpotifyClient:
    def __init__(self):
        self._sp_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SPOTIFY_SCOPES,
            cache_handler=CustomLocalCacheHandler(SPOTIFY_TOKEN_INFO),
            show_dialog=False,
        )
        self._sp_client = spotipy.Spotify(auth_manager=self._sp_oauth)

    def get_now_playing(self):
        try:
            current_track = self._sp_client.current_user_playing_track()
            return self._get_track_info(current_track)
        except Exception as e:
            print("Error fetching Now Playing:", e)
            return {"is_playing": False, "message": "Error fetching Now Playing."}

    def _get_track_info(self, current_track: dict):
        track_info = dict()
        if current_track and current_track.get("is_playing"):
            track_info["track_name"] = current_track["item"]["name"]
            track_info["artist_name"] = ", ".join(
                [artist["name"] for artist in current_track["item"]["artists"]]
            )
            track_info["album_name"] = current_track["item"]["album"]["name"]
            track_info["album_art_url"] = (
                current_track["item"]["album"]["images"][0]["url"]
                if current_track["item"]["album"]["images"]
                else "https://placehold.co/64x64/cccccc/000000?text=No+Art"
            )
            track_info["track_url"] = current_track["item"]["external_urls"]["spotify"]
            track_info["is_playing"] = True
        else:
            track_info["is_playing"] = False
            track_info["message"] = "I'm not listening to anything right now :)"
        return track_info
