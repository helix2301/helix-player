import tkinter as tk
from tkinter import filedialog, simpledialog
import pygame
import os
import vlc

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        
        # Initialize pygame mixer
        pygame.mixer.init()

        # VLC player for streaming
        self.vlc_player = None
        
        # GUI elements
        self.play_button = tk.Button(root, text="play", command=self.play_music)
        self.play_button.pack(pady=10)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=10)

        self.load_button = tk.Button(root, text="Load", command=self.load_music)
        self.load_button.pack(pady=10)

        self.stream_button = tk.Button(root, text="Stream", command=self.stream_music)
        self.stream_button.pack(pady=10)

        # Label for displaying song metadata
        self.metadata_label = tk.Label(root, text="No song loaded", wraplength=300)
        self.metadata_label.pack(pady=20)

        self.music_file = None

        self.music_file = None

    def load_music(self):
        self.music_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if self.music_file:
            pygame.mixer.music.load(self.music_file)
            song_title = os.path.basename(self.music_file)
            self.metadata_label.config(text=f"Loaded: {song_title}")
            print(f"Loaded: {song_title}")

    def play_music(self):
        if self.music_file:
            pygame.mixer.music.play()
            print("Playing music...")

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("Music paused.")

    def stop_music(self):
        pygame.mixer.music.stop()
        print("Music stopped.")

    def stream_music(self):
        stream_url = simpledialog.askstring("Stream URL", "Enter the MP3 stream URL:")
        if stream_url:
            try:
                # Stop any current VLC player
                if self.vlc_player:
                    self.vlc_player.stop()
                
                # Create a new VLC media player for streaming
                self.vlc_player = vlc.MediaPlayer(stream_url)
                self.vlc_player.play()
                print(f"Streaming: {stream_url}")
            except Exception as e:
                print(f"Error streaming URL: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
