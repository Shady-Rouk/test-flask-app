from flask import Flask, render_template
from spotify_client import SpotifyClient

# Initialize the Flask application
app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the landing page of the personal site.
    """
    # Spotify Now Playing info.
    sp_client = SpotifyClient()
    sp_now_playing = sp_client.get_now_playing()

    # Social media links.
    socials = {
        "twitter": "https://x.com/Rouk___",
        "instagram": "https://www.instagram.com/rouk_._",
        "linkedin": "https://www.linkedin.com/in/farouk-balogun",
        "github": "https://github.com/Shady-Rouk",
    }
    return render_template("index.html", socials=socials, sp_now_playing=sp_now_playing)


if __name__ == "__main__":
    # Runs the app in debug mode, which is helpful for development.
    # For production, you would use a proper web server like Gunicorn or uWSGI.
    app.run(debug=True)
