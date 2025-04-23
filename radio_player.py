import subprocess

def play_radio(url):
    subprocess.Popen(['mpv', url, '--no-video'])

def stop_radio():
    subprocess.call(['pkill', 'mpv'])
