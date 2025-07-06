from flask import Flask, render_template, jsonify
from spotify_client import SpotifyClient

# Initialize the Flask application
app = Flask(__name__)

# Spotify client for interacting with the Spotify API.
sp_client = SpotifyClient()


@app.route("/")
def index():
    """
    Renders the landing page of the personal site.
    """

    # Social media links.
    socials = {
        "twitter": "https://x.com/Rouk___",
        "instagram": "https://www.instagram.com/rouk_._",
        "linkedin": "https://www.linkedin.com/in/farouk-balogun",
        "github": "https://github.com/Shady-Rouk",
    }

    # Get the current now-playing data for the initial page load.
    sp_now_playing = sp_client.get_now_playing()

    return render_template("index.html", socials=socials, sp_now_playing=sp_now_playing)


@app.route("/spotify-now-playing")
def spotify_now_playing():
    """
    Returns the current Spotify 'Now Playing' information as JSON.
    This endpoint will be called by JavaScript periodically to get
    the latest now-playing data without refreshing the entire web page.
    """
    # Get the current now-playing data for the initial page load.
    sp_now_playing = sp_client.get_now_playing()
    return jsonify(sp_now_playing)


if __name__ == "__main__":
    # Runs the app in debug mode, which is helpful for development.
    # For production, you would use a proper web server like Gunicorn or uWSGI.
    app.run(debug=True)
