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
        while current:
            marker = "-> " if current == self.current else "   "
            print(f"{marker}{current.data}")
            current = current.next

if __name__ == "__main__":
    playlist = Playlist("My Playlist")

    playlist.add_song("Song 1", "Artist A", "Album X")
    playlist.add_song("Song 2", "Artist B", "Album Y")
    playlist.add_song("Song 3", "Artist C", "Album Z")

    playlist.show_playlist()

    print("\nCurrent:", playlist.get_current_song())

    playlist.next_song()
    print("After next:", playlist.get_current_song())

    playlist.prev_song()
    print("After prev:", playlist.get_current_song())