import tkinter as tk
from tkinter import filedialog, simpledialog
import pygame
import os
import wave
import vlc
import customtkinter
from PIL import Image, ImageTk
from tkinter import *
import random
import time
from tkinter import ttk
from mutagen import File 

pygame.mixer.init()

vlc_player = None
music_file = None
playlist = []
current_index = 0
paused_time = 0  # Initialize paused_time
song_length = 0  # Initialize song_length

root = customtkinter.CTk()
root.title("Helix Music Player")
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')
root.geometry("400x400")

def update_progress_bar():
    if music_file and pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000  # get_pos returns milliseconds
        progress_bar['value'] = (current_time / song_length) * 100  # update progress bar
        countdown_label.config(text=f" {format_time(song_length - current_time)}")  # update countdown
        root.after(1000, update_progress_bar)  # repeat after 1 second

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

def play_music():
    global music_file, song_length, paused_time
    if music_file:
        pygame.mixer.music.play()
        song_length = pygame.mixer.Sound(music_file).get_length()  # Get length of the song
        length_label.config(text=f" {format_time(song_length)}")
        update_progress_bar()  # Start updating the progress bar
        print("Playing music...")


def pause_music():
    global paused_time
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused_time += pygame.mixer.music.get_pos() / 1000  # Add current position to paused_time
        print("Music paused.")

def resume_music():
    global paused_time
    if paused_time > 0:
        pygame.mixer.music.unpause()  # Resume music
        print("Music resumed.")
        update_progress_bar()  # Resume updating the progress bar

def load_music():
    global current_index
    files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.m3u *.pls")])
    if files:
        for file in files:
            if file.endswith('.m3u'):
                load_m3u(file)
            elif file.endswith('.pls'):
                load_pls(file)
            else:
                playlist.append(file)
                playlist_box.insert(tk.END, os.path.basename(file))
        if not music_file:  # Automatically load the first song
            current_index = 0
            load_selected_song(current_index)
            
def load_m3u(m3u_file):
    with open(m3u_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore comments and empty lines
                full_path = os.path.abspath(line)
                playlist.append(full_path)
                playlist_box.insert(tk.END, os.path.basename(full_path))

def load_pls(pls_file):
    with open(pls_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('File'):
                file_path = line.split('=')[1].strip()
                full_path = os.path.abspath(file_path)
                playlist.append(full_path)
                playlist_box.insert(tk.END, os.path.basename(full_path))

def load_selected_song(index):
    global music_file, current_index
    if 0 <= index < len(playlist):
        music_file = playlist[index]
        pygame.mixer.music.load(music_file)
        metadata_label.config(text=os.path.basename(music_file))
        current_index = index

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

def select_song(event):
    selection = playlist_box.curselection()
    if selection:
        load_selected_song(selection[0])
        play_music()

def next_song():
    global current_index
    if current_index + 1 < len(playlist):
        current_index += 1
        load_selected_song(current_index)
        play_music()

def back_song():
    global current_index
    if current_index - 1 >= 0:
        current_index -= 1
        load_selected_song(current_index)
        play_music()

def shuffle_playlist():
    global current_index
    if playlist:
        random.shuffle(playlist)  
        playlist_box.delete(0, tk.END)  
        for song in playlist:
            playlist_box.insert(tk.END, os.path.basename(song))  
        current_index = 0  
        load_selected_song(current_index)

metadata_label = tk.Label(root, text="No song loaded", wraplength=300, bg="gray75", width=38, height=2 ,font='Helvetica 14 bold')
metadata_label.pack(pady=10)
metadata_label.place(x=10, y=10)

# Playlist Listbox
playlist_box = Listbox(root, width=51, height=10, bg="black", fg="white", font='Helvetica 12')
playlist_box.pack(pady=10)
playlist_box.bind('<<ListboxSelect>>', select_song)
playlist_box.place(x=10, y=100)

play_photo = PhotoImage(file='icons8-play-20.png')
play_button = customtkinter.CTkButton(root, image=play_photo, text="",command=play_music, width=40,height=10)
play_button.pack(pady=1)
play_button.place(x=10, y=62)
        
pause_photo = PhotoImage(file='icons8-pause-20.png')
pause_button = customtkinter.CTkButton(root, image=pause_photo, command=pause_music, text="", width=40,height=10)
pause_button.pack(pady=1)
pause_button.place(x=54, y=62)

stop_photo = PhotoImage(file='icons8-stop-20.png')
stop_button = customtkinter.CTkButton(root, image=stop_photo, text="", command=stop_music, width=40,height=10)
stop_button.pack(pady=1)
stop_button.place(x=98, y=62)

back_photo = PhotoImage(file='icons8-back-20.png')
back_button = customtkinter.CTkButton(root, image=back_photo,text="", command=back_song, width=40, height=10)
back_button.pack(pady=1)
back_button.place(x=141, y=62)

next_photo = PhotoImage(file='icons8-forward-20.png')
next_button = customtkinter.CTkButton(root, image=next_photo, text="", command=next_song, width=40, height=10)
next_button.pack(pady=1)
next_button.place(x=184, y=62)

shuffle_photo = PhotoImage(file='icons8-shuffle-20.png')
shuffle_button = customtkinter.CTkButton(root, image=shuffle_photo, text="", command=shuffle_playlist, width=40, height=10)
shuffle_button.pack(pady=1)
shuffle_button.place(x=228, y=62) 

load_photo = PhotoImage(file='icons8-eject-20.png')
load_button = customtkinter.CTkButton(root, image=load_photo, text="", command=load_music, width=40,height=10)
load_button.pack(pady=1)
load_button.place(x=380, y=62)

stream_photo = PhotoImage(file='icons8-stream-20.png')
stream_button = customtkinter.CTkButton(root, image=stream_photo,text="", command=stream_music, width=40,height=10)
stream_button.pack(pady=1)
stream_button.place(x=430, y=62)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)
progress_bar.place(x=90, y=300)

length_label = tk.Label(root, text="0:00", bg="gray75")
length_label.pack()
length_label.place(x=395, y=300)

countdown_label = tk.Label(root, text="0:00", bg="gray75")
countdown_label.pack()
countdown_label.place(x=50, y=300)

root.mainloop()
