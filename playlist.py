from ll import DoublyLinkedList
from time import perf_counter
from memory_profiler import profile


class Song:
    def __init__(self, name, artist, album):
        self.name = name
        self.artist = artist
        self.album = album

    def __str__(self):
        return f"{self.name} - {self.artist} ({self.album})"


class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = DoublyLinkedList()
        self.current = None

    def add_song(self, name, artist, album):
        song = Song(name, artist, album)
        self.songs.append(song)
        if self.current is None:
            self.current = self.songs.head

    def remove_song(self, name):
        current = self.songs.head
        while current:
            if current.data.name == name:
                if current == self.current:
                    self.current = current.next or current.prev
                self.songs.remove(current.data)
                return True
            current = current.next
        return False

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next
        return self.get_current_song()

    def prev_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
        return self.get_current_song()

    def get_current_song(self):
        if self.current:
            return str(self.current.data)
        return None

    def show_playlist(self):
        current = self.songs.head
        index = 1
        while current:
            marker = "-> " if current == self.current else "   "
            print(f"{marker}{index:03d}. {current.data}")
            current = current.next
            index += 1


# --------- DATA GENERATION (100 canciones dinámicas) ---------
def build_song_data():
    artists = [
        "The Weeknd", "Bad Bunny", "Taylor Swift", "Karol G", "Billie Eilish",
        "Harry Styles", "Dua Lipa", "Rosalia", "BTS", "Olivia Rodrigo"
    ]

    albums = [
        "After Hours", "Un Verano Sin Ti", "Midnights", "Mañana Será Bonito",
        "Happier Than Ever", "Harry's House", "Future Nostalgia", "Motomami",
        "Butter", "SOUR"
    ]

    songs = []

    for i in range(1, 101):
        name = f"Song {i:03d}"
        artist = artists[(i - 1) % len(artists)]
        album = albums[(i - 1) % len(albums)]
        songs.append((name, artist, album))

    return songs


# Perfilado usando el decorador

@profile
def load_playlist(playlist):
    for name, artist, album in build_song_data():
        playlist.add_song(name, artist, album)
    return playlist

if __name__ == "__main__":
    start = perf_counter()

    playlist = load_playlist(Playlist("My Playlist"))

    elapsed = perf_counter() - start

    print(f"\nTiempo de carga: {elapsed:.6f} segundos")
    print(f"Loaded {len(playlist.songs)} songs\n")

    playlist.show_playlist()

    print("\nCurrent:", playlist.get_current_song())

    playlist.next_song()
    print("After next:", playlist.get_current_song())

    playlist.prev_song()
    print("After prev:", playlist.get_current_song())