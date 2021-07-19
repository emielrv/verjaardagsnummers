import os
from pydub import AudioSegment

person = 'El'

name_moments = [8.7, 25.1, 64.1, 80.5, 119.5, 136.0, 154.4, 170.8]
custom_song_input = [os.path.join(f"input/{person}/{f}") for f in os.listdir(f"input/{person}") if f.endswith('.ogg')]

interval_duration = 0.9 * 1000
name_moments_ms = [moment * 1000 for moment in name_moments]


def fade_name(song, moment, interval):
    return song[:moment] + \
           (song[moment:moment + interval] - 12) + \
           song[moment + interval:]


def process_custom_song(filename):
    sound = AudioSegment.from_file(filename)
    trimmed_sound = sound.strip_silence(silence_len=10, silence_thresh=-50, padding=10)
    speed = len(trimmed_sound) / (interval_duration)
    if speed < 1:
        chunk_size = len(trimmed_sound)
    else:
        chunk_size = 150
    result = trimmed_sound.speedup(speed, chunk_size=chunk_size, crossfade=10)
    return result


if __name__ == "__main__":
    song = AudioSegment.from_mp3("hekanjer.mp3")

    input_songs = []
    for input_file in custom_song_input:
        input_songs.append(process_custom_song(input_file))

    for moment in name_moments_ms:
        song = fade_name(song, moment, interval_duration)
        for custom in input_songs:
            song = song.overlay(custom, position=moment)

    song.export(f"results/{person} Birthday Boy.mp3", format="mp3")
