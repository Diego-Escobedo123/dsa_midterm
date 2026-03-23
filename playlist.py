from time import perf_counter
import random

from memory_profiler import profile

from ll import DoublyLinkedList


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
        self.shuffle_enabled = False
        self._shuffle_order = []
        self._shuffle_index = 0

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
                self._rebuild_shuffle_order(keep_current=True)
                return True
            current = current.next
        return False

    def _nodes_in_order(self):
        nodes = []
        current = self.songs.head
        while current:
            nodes.append(current)
            current = current.next
        return nodes

    def _rebuild_shuffle_order(self, keep_current=True):
        nodes = self._nodes_in_order()
        if not nodes:
            self._shuffle_order = []
            self._shuffle_index = 0
            self.current = None
            return

        if keep_current and self.current in nodes:
            current_node = self.current
        else:
            current_node = nodes[0]
            self.current = current_node

        remaining = [node for node in nodes if node is not current_node]
        random.shuffle(remaining)
        self._shuffle_order = [current_node] + remaining
        self._shuffle_index = 0

    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        if self.shuffle_enabled:
            self._rebuild_shuffle_order(keep_current=True)
        return self.shuffle_enabled

    def play(self):
        if self.current is None and self.songs.head is not None:
            self.current = self.songs.head
        return self.get_current_song()

    def next_song(self):
        if self.current is None:
            return self.play()

        if not self.shuffle_enabled:
            if self.current.next:
                self.current = self.current.next
            return self.get_current_song()

        if not self._shuffle_order or self.current not in self._shuffle_order:
            self._rebuild_shuffle_order(keep_current=True)

        if self._shuffle_index + 1 < len(self._shuffle_order):
            self._shuffle_index += 1
            self.current = self._shuffle_order[self._shuffle_index]
        else:
            self._rebuild_shuffle_order(keep_current=True)
            if len(self._shuffle_order) > 1:
                self._shuffle_index = 1
                self.current = self._shuffle_order[self._shuffle_index]

        return self.get_current_song()

    def prev_song(self):
        if self.current is None:
            return self.play()

        if not self.shuffle_enabled:
            if self.current.prev:
                self.current = self.current.prev
            return self.get_current_song()

        if not self._shuffle_order or self.current not in self._shuffle_order:
            self._rebuild_shuffle_order(keep_current=True)

        if self._shuffle_index > 0:
            self._shuffle_index -= 1
            self.current = self._shuffle_order[self._shuffle_index]

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


@profile
def load_playlist(playlist):
    for name, artist, album in build_song_data():
        playlist.add_song(name, artist, album)
    return playlist


def print_menu(playlist):
    print("\n=== Playlist Player ===")
    print(f"Playlist: {playlist.name}")
    print(f"Shuffle: {'ON' if playlist.shuffle_enabled else 'OFF'}")
    print("1. Play")
    print("2. Next")
    print("3. Previous")
    print("4. Toggle Shuffle")
    print("5. Show Playlist")
    print("6. Quit")


if __name__ == "__main__":
    start = perf_counter()
    playlist = load_playlist(Playlist("My Playlist"))
    elapsed = perf_counter() - start

    print(f"\nTiempo de carga: {elapsed:.6f} segundos")
    print(f"Loaded {len(playlist.songs)} songs")

    while True:
        print_menu(playlist)
        option = input("Choose an option: ").strip()

        if option == "1":
            print("\nNow playing:", playlist.play())

        elif option == "2":
            print("\nNext:", playlist.next_song())

        elif option == "3":
            print("\nPrevious:", playlist.prev_song())

        elif option == "4":
            state = playlist.toggle_shuffle()
            print(f"\nShuffle {'enabled' if state else 'disabled'}")
            print("Now playing:", playlist.get_current_song())

        elif option == "5":
            print()
            playlist.show_playlist()

        elif option == "6":
            print("\nGoodbye!\n")
            break

        else:
            print("\nInvalid option. Try again.")