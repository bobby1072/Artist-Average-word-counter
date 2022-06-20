import json
import tkinter as tk
import re
import requests
import musicbrainzngs
def get_average_word_count(artist_name) -> str:
    try:
        musicbrainzngs.set_useragent("artist music", "0.1", "bobby")
        old_result = musicbrainzngs.search_artists(
            artist="" + artist_name)  # making a search request using the 'artist' parameter which returns all registered artists similar
        for artist in old_result['artist-list']:
            if artist["name"].lower() == artist_name.lower():
                real_id = [artist["id"], artist["name"]]
        result = musicbrainzngs.get_artist_by_id(real_id[0], includes=[
            "recordings"])  # request to return artist details and recordings list
    except:
        1+1
    # converting result to json(dictionary) format. dictionary is pytohns closest equivalent to JSON formatting.
    jsresult = json.dumps(result)
    jsresult = json.loads(jsresult)
    #
    # this block adds every song title to the 'song_arr array'
    # using the recording list is the closest data to every song that artist has.
    song_arr = []
    for x in range(0, len(jsresult["artist"]["recording-list"])):
        song_arr.append(jsresult["artist"]["recording-list"][x]["title"])
    song_arr = list(
        dict.fromkeys(song_arr))  # this converts the array to a dictionary then back to a list to remove duplicate values.
    #
    # block to request lyrics for each song from the lyricsovh api
    all_lyrics = []
    for n in range(0, len(song_arr)):
        lyrics = requests.get("https://api.lyrics.ovh/v1/" + str(real_id[1]) + "/" + song_arr[n])
        if r'"error"' not in str(lyrics.text):
            all_lyrics.append(lyrics.text)  # adding the lyrics for each song to new array
    #
    # this blocks cleans the data and leaves you with an array with in theory only the word from the lyrics that are finadable
    lyricsonly = []
    for p in range(0, len(all_lyrics)):
        if r'"error"' not in str(all_lyrics[p]) and "<!DOCTYPE" not in str(all_lyrics[p]) and "lyrics" in str(all_lyrics[p]):
            jvar = json.loads(str(all_lyrics[p]))
            try:
                word_var = str(jvar['lyrics'])
                word_var = re.sub("[^0-9a-zA-Z]+", " ", word_var)  # removing the non alphanumeric characters
                lyricsonly.append(word_var)
            except KeyError:
                1 + 1
    #
    # block to calculate number of words in each song
    word_coun = 0
    word_coun_arr = []
    for q in range(0, len(lyricsonly)):
        word_var = str(lyricsonly[q])
        ly_arr = []
        indiv_wordvar = ""
        for xx in range(0, len(word_var)):
            if word_var[xx] != " ":
                indiv_wordvar = indiv_wordvar + str(word_var[xx])
            else:
                ly_arr.append(indiv_wordvar)
                indiv_wordvar = ""
        for zz in range(0, len(ly_arr)):
            word_coun = word_coun + 1
        word_coun_arr.append(word_coun)
    final_avg = 0
    #
    # block to calculate the average for all songs
    for ii in range(0, len(word_coun_arr)):
        final_avg = final_avg + word_coun_arr[ii]
    final_avg = final_avg / len(word_coun_arr)
    name_avgcoun = [real_id[1], final_avg // 1]
    return name_avgcoun
def gui() -> tk.Tk:
    """Set up a Tkinter GUI and return the window."""
    window = tk.Tk()
    window.geometry("")
    window.title("avg word counter")
    tk.Label(
        window,
        text="please enter the artist you like the average word count for:"
    ).grid(row=0, sticky="w")

    # Need to assign artist entry and word count labels to variables
    # so we can read the user's text entry and change the label.
    artist_entry = tk.Entry(window)
    artist_entry.grid(row=0, column=1, sticky="w")
    word_count_label = tk.Label(
        window,
        text="Enter an artist and click 'search' to find the average word count."
    )
    word_count_label.grid(row=4, sticky="w")

    # This nested function has access to read or mutate the variables in the
    # 'gui' function. It's what's called a 'closure'.
    def set_lyric_label():
        """Set the Tkinter lyric label to an artist's average word count."""
        artist_name = artist_entry.get()
        if artist_name:
            avg_word_count = get_average_word_count(artist_name)
            word_count_label.config(text=f"{avg_word_count[0]}'s average word count is {avg_word_count[1]}")
        else:
            word_count_label.config(text=f"You must enter an artist's name.")

    tk.Button(
        text="search",
        command=set_lyric_label
    ).grid(row=3, column=1)

    return window


# This 'if __name__ == "__main__"' block means that if we just want to import the function to get
# word count, we won't set up a GUI. It's called an 'entrypoint'.
if __name__ == "__main__":
    master = gui()
    master.mainloop()
