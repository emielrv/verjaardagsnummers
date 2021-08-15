import os
from pydub import AudioSegment

person = 'Jeffrey'
song = 'samson'

intro_trim = None
volume_change = None

if song == 'hekanjer':
    # Download song here: https://www.youtube.com/watch?v=xiV4dkoNWrc
    mp3 = "hekanjer.mp3"
    name_moments = [8.7, 25.1, 64.1, 80.5, 119.5, 136.0, 154.4, 170.8]
    version = 'v1'
    interval_duration = 0.9 * 1000
elif song == 'samson':
    # Download song here: https://open.spotify.com/track/3Lj5XGCR6z76T0Wu5ugRVA?si=0e6b43a638ff4c07
    # Please note our recording was off by +/- one second
    mp3 = "samson.mp3"
    name_moments = [14.9, 30.3, 76.8, 92.4, 107.9, 123.3]
    version = 'v2'
    interval_duration = 0.64 * 1000
    intro_trim = 78500
    volume_change = 7
else:
    raise NameError(f"song not found: {song}")


def fade_name(song, moment, interval):
    return song[:moment] + \
           (song[moment:moment + interval] - 12) + \
           song[moment + interval:]


def process_custom_song(filename):
    sound = AudioSegment.from_file(filename)
    trimmed_sound = sound.strip_silence(silence_len=10, silence_thresh=-50, padding=10)
    speed = len(trimmed_sound) / interval_duration
    if speed < 1:
        chunk_size = len(trimmed_sound)
    else:
        chunk_size = 150
    result = trimmed_sound.speedup(speed, chunk_size=chunk_size, crossfade=10)
    return result


if __name__ == "__main__":
    song = AudioSegment.from_mp3(mp3)
    custom_song_input = [os.path.join(f"input/{person}/{f}") for f in os.listdir(f"input/{person}") if
                         f.endswith('.ogg')]
    name_moments_ms = [moment * 1000 for moment in name_moments]

    input_songs = []
    for input_file in custom_song_input:
        input_songs.append(process_custom_song(input_file))

    if intro_trim:
        song = song[intro_trim:]

    if volume_change:
        song = song + volume_change

    for moment in name_moments_ms:
        song = fade_name(song, moment, interval_duration)
        for custom in input_songs:
            song = song.overlay(custom, position=moment)

    song.export(f"results/{person} Birthday Boy {version}.mp3", format="mp3")
