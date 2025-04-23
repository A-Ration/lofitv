from flask import Flask, render_template, send_from_directory
import os
from news import get_headlines
from weather import get_weather
from generate_art import generate_art_from_headline

app = Flask(__name__)

@app.route('/')
def index():
    weather = get_weather("Philadelphia,US")
    headlines = get_headlines("home")[:7]
    top_headline = headlines[0]['title']


    art_path = generate_art_from_headline(top_headline)
    art_file = os.path.basename(art_path) if art_path else None

    return render_template("index.html",
                           weather=weather,
                           headline=top_headline,
                           art_file=art_file)

@app.route('/static/art/<filename>')
def serve_art(filename):
    return send_from_directory('static/art', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
