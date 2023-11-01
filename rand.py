import os
import random
from pydub import AudioSegment
import keyboard
import time
import tempfile
import pygame

# Function to play a random song
def play_random_song(music_folder, previous_song, temp_file):
    music_files = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.mp4'))]

    # change song
    new_song = random.choice(music_files)
    while new_song == previous_song:
        new_song = random.choice(music_files)

    song_path = os.path.join(music_folder, new_song)

    #os.system(f'start "" "{song_path}"') FOR THE WINDOW POPUP

    sound = AudioSegment.from_file(song_path)

    # Use a unique temporary file for each song ;)
    temp_filename = os.path.join(temp_file, f"{new_song}.mp3")
    sound.export(temp_filename, format="mp3")

    pygame.mixer.music.load(temp_filename)
    pygame.mixer.music.play()

    return new_song

if __name__ == "__main__":
    music_folder = "C:/Users/Path/Music" # Folder path
    temp_folder = tempfile.mkdtemp()  # Create a temporary folder for the song files
    previous_song = None

    # Start song
    trigger_key = "9"

    # Pause key
    pause_key = "8"

    # Stop process
    stop_key = "0"

    pygame.mixer.init()

    # Pause and resume functions
    is_paused = False

    def pause_resume(e):
        global is_paused
        if is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
        else:
            pygame.mixer.music.pause()
            is_paused = True

    def stop_script(e):
        pygame.mixer.music.stop()
        global stop_requested
        stop_requested = True


    # Pause key event
    keyboard.on_press_key(pause_key, pause_resume)

    # Stop key event
    keyboard.on_press_key(stop_key, stop_script)


    stop_requested = False

    while not stop_requested:
        keyboard.wait(trigger_key)
        if not stop_requested:
            previous_song = play_random_song(music_folder, previous_song, temp_folder)
            time.sleep(1)  # Add a delay to prevent multiple songs from playing with a single key press

    # Clean up and exit
    keyboard.unhook_all()
