import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        # Use absolute path to avoid FileNotFoundError
        self.music_folder = os.path.abspath(music_folder)
        if not os.path.exists(self.music_folder):
            raise FileNotFoundError(f"Music folder not found: {self.music_folder}")
        self.playlist = self.load_music()
        self.current_index = 0
        self.is_playing = False

    def load_music(self):
        files = [f for f in os.listdir(self.music_folder) if f.endswith(('.wav', '.mp3'))]
        files.sort()  # optional: sort alphabetically
        return files

    def play(self):
        if not self.playlist:
            return
        track = self.playlist[self.current_index]
        pygame.mixer.music.load(os.path.join(self.music_folder, track))
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track(self):
        if not self.playlist:
            return "No tracks"
        return self.playlist[self.current_index]

    def get_position(self):
        if self.is_playing:
            return pygame.mixer.music.get_pos() // 1000
        return 0