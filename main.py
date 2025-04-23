import pygame
import time
import json
import datetime
from weather import get_weather
from news import get_headlines
from generate_art import generate_art_from_headline
from radio_player import play_radio, stop_radio

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pi Cable Station")
font = pygame.font.Font(None, 48)
ticker_font = pygame.font.Font(None, 36)

with open("config.json") as f:
    config = json.load(f)

station = config["radio_station"]
play_radio(station["url"])

# Timing setup
start_time = time.time()
headline_index = 0
image_timer = 0
fade_duration = 2.0  # seconds

# Initial pulls
weather = get_weather(config["location"], config["weather_units"])
headlines = get_headlines(config["nyt_section"])[:7]
headline_text = headlines[headline_index]["title"]
art_path = generate_art_from_headline(headline_text)

# Load image
def load_image(path):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (400, 400))

image = load_image(art_path) if art_path else None
last_fade = 0

def fade_in(surface, image, pos, duration):
    clock = pygame.time.Clock()
    for alpha in range(0, 256, 8):
        temp_img = image.copy()
        temp_img.set_alpha(alpha)
        screen.fill((10, 10, 10))
        draw_static_elements()
        surface.blit(temp_img, pos)
        pygame.display.flip()
        clock.tick(60)

def draw_static_elements():
    # Headline
    title = font.render(headline_text, True, (255, 255, 255))
    screen.blit(title, (50, 50))

    # Weather
    weather_text = font.render(
        f"{weather['temp']}°F, {weather['description']}", True, (200, 200, 200)
    )
    screen.blit(weather_text, (50, 150))

    # Radio info
    radio_text = font.render(
        f"Now Playing: {station['name']}", True, (180, 180, 255)
    )
    screen.blit(radio_text, (50, 250))

    # Ticker (shortened headline)
    ticker = ticker_font.render(f"Latest: {headline_text}", True, (255, 215, 0))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 680, 1280, 40))
    screen.blit(ticker, (20, 685))

running = True
while running:
    now = time.time()
    elapsed = now - start_time
    minutes = elapsed // 60

    # Every 5 minutes: next headline
    if minutes % 5 == 0 and headline_index != int(minutes / 5) % 7:
        headline_index = int(minutes / 5) % 7
        headline_text = headlines[headline_index]["title"]

    # Every 20 minutes: new image from current headline
    if minutes % 20 == 0 and int(minutes) != last_fade:
        last_fade = int(minutes)
        art_path = generate_art_from_headline(headline_text)
        if art_path:
            image = load_image(art_path)
            fade_in(screen, image, (800, 200), fade_duration)

    # Every 60 minutes: refresh everything
    if minutes % 60 == 0 and int(minutes) != image_timer:
        image_timer = int(minutes)
        weather = get_weather(config["location"], config["weather_units"])
        headlines = get_headlines(config["nyt_section"])[:7]
        headline_index = 0
        headline_text = headlines[headline_index]["title"]
        art_path = generate_art_from_headline(headline_text)
        if art_path:
            image = load_image(art_path)
            fade_in(screen, image, (800, 200), fade_duration)

    # Draw screen
    screen.fill((10, 10, 10))
    draw_static_elements()
    if image:
        screen.blit(image, (800, 200))
    pygame.display.flip()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_radio()
            running = False

    time.sleep(1)
