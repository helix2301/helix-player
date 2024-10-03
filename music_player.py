import tkinter as tk
from tkinter import filedialog, simpledialog
import pygame
import os
import vlc
import customtkinter
from PIL import Image, ImageTk
from tkinter import *

pygame.mixer.init()

vlc_player = None
music_file = None

root = customtkinter.CTk()
root.title("Simple Music Player")
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')
root.geometry("200x300")

def play_music():
    global music_file
    if music_file:
        pygame.mixer.music.play()
        print("Playing music...")

def pause_music():
        global music_file
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("Music paused.")

def load_music():
    global music_file
    music_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
    if music_file:
        pygame.mixer.music.load(music_file)
        song_title = os.path.basename(music_file)
        metadata_label.config(text=f" {song_title}")
        print(f" {song_title}")

def stop_music():
        global music_file
        pygame.mixer.music.stop()
        print("Music stopped.")

def stream_music():
        global vlc_player
        stream_url = simpledialog.askstring("Stream URL", "Enter the MP3 stream URL:")
        if stream_url:
            try:
                # Stop any current VLC player
                if vlc_player:
                    vlc_player.stop()
                
                # Create a new VLC media player for streaming
                vlc_player = vlc.MediaPlayer(stream_url)
                vlc_player.play()
                print(f"Streaming: {stream_url}")
            except Exception as e:
                print(f"Error streaming URL: {e}")

metadata_label = tk.Label(root, text="No song loaded", wraplength=300)
metadata_label.pack(pady=20)
metadata_label.place(x=10, y=10)

play_photo = PhotoImage(file='icons8-play-20.png')
play_button = customtkinter.CTkButton(root, image=play_photo, text="",command=play_music, width=40,height=10)
play_button.pack(pady=1)
play_button.place(x=10, y=45)
        
pause_photo = PhotoImage(file='icons8-pause-20.png')
pause_button = customtkinter.CTkButton(root, image=pause_photo, command=pause_music, text="", width=40,height=10)
pause_button.pack(pady=1)
pause_button.place(x=54, y=45)

stop_photo = PhotoImage(file='icons8-stop-20.png')
stop_button = customtkinter.CTkButton(root, image=stop_photo, text="", command=stop_music, width=40,height=10)
stop_button.pack(pady=1)
stop_button.place(x=98, y=45)

load_photo = PhotoImage(file='icons8-eject-20.png')
load_button = customtkinter.CTkButton(root, image=load_photo, text="", command=load_music, width=40,height=10)
load_button.pack(pady=1)
load_button.place(x=155, y=45)

stream_photo = PhotoImage(file='icons8-stream-20.png')
stream_button = customtkinter.CTkButton(root, image=stream_photo,text="", command=stream_music, width=40,height=10)
stream_button.pack(pady=1)
stream_button.place(x=210, y=45)

#metadata_label = tk.Label(root, text="No song loaded", wraplength=300)
#metadata_label.pack(pady=20)

#root = tk.Tk()
#music_player = MusicPlayer(root)
root.mainloop()