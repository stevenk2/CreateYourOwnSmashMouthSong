# Coding exercise part 1 -
# given a .txt file containing the lyrics of a given song,
# your program should output a data structure that tells me how often each word in the song is used.
# So for the All Star Lyrics file, your data structure will have a value of 1 for the word
# "thumb" and 5 for "gold"..

#Part 2 -
# Expanding on what you have already, your program should get the word counts for each song.
# These should not be aggregated, but on a per-song basis (i.e. don't store the number of
# "the"s across all the songs, but rather, each song should have its own word frequency counts).
# You should still only have one data structure at the end.

# Part 3 -
# We're moving on to part 3 of the exercise! First, we want more info about the songs.
# For each song, we want to know how many words the average line is and how many lines the song has
# (empty lines don't count as lines, so if a line is just "\n" in the .txt, we should not count it).
# We might add more information later as well.
# More importantly, we want to be able to identify the chorus of the song.
# For each song, you should save off the actual text of the chorus, how many words the average
# line in the chorus is and how many lines the chorus is (same as we did for the whole song),
# and the number of times the chorus happens in the song.

# Part 4 -
# In part 4, you'll be setting up the beginnings of what's called a Markov chain.
# For each song, you'll create a data structure that holds the number of instances
# each word is followed by another in each song. Which is a lot of words, so let's do an example.
# If we take the line "not all that glitters is gold and gold again",
# we'd want the data structure to know that
# "Not" is followed by "all" 1 time
# "All" is followed by "that" 1 time
# "That" is followed by "glitters" 1 time
# "Glitters is followed by "is" 1 time
# "Is" is followed by "gold" time
# "Gold" is followed by "and" 1 time and "again" 1 time
# "And" is followed by "gold" 1 time
# This pattern will be line-agnostic, so for instance if the next line is
# "only shooting stars break the mold", then we would also say that
# "Again" is followed by "only" 1 time
# Since "again" ends the first line and "only" starts the second line
# (we just don't care about lines, basically).
# This data structure will be stored as part of each song's information.


import re
import os
import pprint
pp = pprint.PrettyPrinter()

# Parts 1 and 2
all_songs_dict = {}

for file in os.listdir('C:/Users/Katie/Desktop/Data Science/Kevin projects/Project 1'):
    if file.endswith(".txt"):
        song_name = os.path.join(file)
        with open(song_name, "r") as lyrics:
            all_lines = lyrics.readlines()
            word_dict = {}
            for line in all_lines:
                if line == "\n":
                    continue
                no_return = line.strip()
                no_extra_char = re.sub('[()?!"]', '', no_return)
                word_list = no_extra_char.split(" ")
                for word in word_list:
                    lowercase_word = word.lower()
                    if word_dict.get(lowercase_word) == None:
                        word_dict[lowercase_word] = 1
                    else:
                        word_dict[lowercase_word] += 1
            all_songs_dict[song_name] = word_dict

#pp.pprint(all_songs_dict)

# Parts 3 and 4
song_info = {}
for file in os.listdir('C:/Users/Katie/Desktop/Data Science/Kevin projects/Project 1'):
    if file.endswith(".txt"):
        # Setting up dictionaries. The big dict will be song_info, and the keys of that dict will be the
        # song name and the values will be each of these dictionaries.
        song_num_lines = {}
        song_avg_words_per_line = {}
        chorus_lyrics = {}
        chorus_avg_words_per_line = {}
        chorus_num_lines = {}
        markov_chain = {}
        song_name = os.path.join(file)
        # print(song_name)
        with open(song_name, "r") as lyrics:
            all_lines = lyrics.readlines()
            all_lines_cleaned = []
            line_count = 0
            song_word_count = 0
            song_chorus_dict = {}
            song_markov_chain = {}
            previous_word = ""
            for line in all_lines:
                # Removing all returns and stripping lines
                if line == "\n":
                    continue
                no_extra_char = re.sub('[()?!"]', '', line)
                stripped_line = no_extra_char.replace("--", "").strip()
                # Adding to clean list
                all_lines_cleaned.append(stripped_line)
                # Adding to the line_count for this specific song
                line_count += 1
                if stripped_line in song_chorus_dict:
                    song_chorus_dict[stripped_line] +=1
                else:
                    song_chorus_dict[stripped_line] = 1
                words = stripped_line.split(" ")
                # Adding to the word totals for this song to find the average
                for word in words:
                    word = word.lower()
                    song_word_count += 1
                    word_markov_chain = {}
                # Markov chain
                    if previous_word == "":
                        previous_word = word
                        continue
                    if previous_word in song_markov_chain:
                        word_markov_chain = song_markov_chain.get(previous_word)
                        if word in word_markov_chain:
                            word_markov_chain[word] += 1
                        else:
                            word_markov_chain[word] = 1
                        song_markov_chain[previous_word] = word_markov_chain

                    else:
                        word_markov_chain[word] = 1
                        song_markov_chain[previous_word] = word_markov_chain
                    previous_word = word

            # Removing lines that only show up once in a song
            new_song_chorus_dict = {k:v for k,v in song_chorus_dict.items() if v != 1}
            #print(new_song_chorus_dict)
            #print(all_lines_cleaned)
            word_count_avg = song_word_count/line_count
            # Adding to the individual dictionaries with the Keys as the definitions
            song_avg_words_per_line["Average words per line in song"] = word_count_avg
            song_num_lines["Number of Lines in Song"] = line_count
            markov_chain["Markov Chain"] = song_markov_chain
            #print(song_markov_chain)
        #print(song_num_lines)
        #print(song_avg_words_per_line)
        # Adding to the part song_info dictionary
        song_info[song_name] = song_avg_words_per_line, song_num_lines, markov_chain
print(song_info)




