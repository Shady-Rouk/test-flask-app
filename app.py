from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the landing page of the personal site.
    """
    # Social media links.
    socials = {
        "twitter": "https://x.com/Rouk___",
        "instagram": "https://www.instagram.com/rouk_._",
        "linkedin": "https://www.linkedin.com/in/farouk-balogun",
        "github": "https://github.com/Shady-Rouk"
    }
    return render_template('index.html', socials=socials)

if __name__ == '__main__':
    # Runs the app in debug mode, which is helpful for development.
    # For production, you would use a proper web server like Gunicorn or uWSGI.
    app.run(debug=True)
