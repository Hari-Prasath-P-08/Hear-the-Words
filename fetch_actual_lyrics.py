import lyricsgenius
import os

genius = lyricsgenius.Genius("5bAOLbrkrJZwElNy9iUkp3zu3x9Wb-KeH__DIpjsCxBfViB7L_0Tn9oX6-hQyfsN")
song = genius.search_song("Believer", "Imagine Dragons")
if song:
    lyrics = song.lyrics
    os.makedirs("actual_lyrics", exist_ok=True)
    with open("actual_lyrics/Believer_actual.txt", "w", encoding="utf-8") as f:
        f.write(lyrics)
    print("Lyrics saved!")
else:
    print("Song not found.")