#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import time
from collections import Counter


#Collects the lyrics from the website lyrics.com, and analyses it in different ways.


def GetLyrics(fileName, runs):  #the function that gets the lyrics and outputs it to a txt file in the directory
    url = "https://www.lyrics.com/random.php" #the random song url
    allLyrics = []
    start = time.time() 
    hitPer = []
    for i in range(runs): #each run takes aprox. 1.5 seconds, aka 5000 songs takes 2 hours
        if round(i*100/runs) % 20 == 0 and (i*100/runs) not in hitPer and (i*100/runs) % 1 == 0: #Prints out the operations progress every 5%
            print(str(i*100/runs) + "%")
            hitPer.append(i*100/runs)
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser") 
        try:
            songLyrics = soup.find(id="lyric-body-text").text #fins the element with the lyrics in it
            allLyrics.append(songLyrics)
        except:
            pass
        
    f = open(fileName, "w+")
    for song in allLyrics:
        try:
            f.write(song)
        except:
            pass
    f.close()
    end = time.time()
    print(str(runs), "songs took", str(end-start), "seconds\n") #prints out how long the scrape took


def WordAnalyse(fileName, punctuation): #Analyses how often the most common words occur
    f = open(fileName, "r")
    lines = f.readlines() #read the text file with the lyrics in it.
    f.close()
    allWords = []
    for line in lines:
        words = line.replace("\n", "").split(" ")
        for word in words:
            if word != "":
                for character in punctuation: #removes all the characters in the punctuation list from the word
                    word = word.replace(character, "")
                allWords.append(word.lower().replace("?", "").replace("!", "").replace(",", ""))
            
    freqWords = Counter(allWords).most_common()[:5] #gets the 100 most common words
    for index, freqWord in enumerate(freqWords):
        freqWord, occurances = freqWord
        print("Word # " + str(index) + ": " + str(freqWord) + " occured " + str(occurances) + " times") #prints them out in order
    print("")


def LetterAnalyse(fileName, punctuation):  #Analyses how often the most common letters are, the same procces as the words
    f = open(fileName, "r")
    lines = f.readlines()
    f.close()
    allLetters = []
    for line in lines:
        words = line.replace("\n", "").split(" ")
        for word in words:
            if word != "":
                letters = list(word.lower())
                for letter in letters:
                    if letter not in punctuation:
                        allLetters.append(letter)
    freqLetters = Counter(allLetters).most_common()[:5] #gives 40 most common
    for index, freqLetter in enumerate(freqLetters):
        freqLetter, occurances = freqLetter
        print("Letter # " + str(index) + ": " + str(freqLetter) + " occured " + str(occurances) + " times")
    print("")

def LineAnalyse(fileName, punctuation):  #gives most common lines, only works with large data set (3000 songs+), as repetitive songs will change results
    f = open(fileName, "r")
    lines = f.readlines()
    f.close()
    allLines = []
    for line in lines:
        for character in punctuation:
            line = line.replace(character, "")
        if line != "" and line != " " and "chorus" not in line.lower(): #removes unwanted data
            allLines.append(line.lower())
        
    freqLines = Counter(allLines).most_common()[:5]
    for index, freqLines in enumerate(freqLines):
        freqLines, occurances = freqLines
        print("Line # " + str(index) + ': "' + str(freqLines) + '" occured ' + str(occurances) + " times")
    print("")

punctuation = ["!", '"', "'", "£", ".", "(", ")", "-", ",", "[", "]", ":", ";", "\n", "?", "’"]   #all the different characters not wanted
runs = int(input("How many songs to be scanned: "))
fileName = str(runs) + "-song-lyrics.txt"
GetLyrics(fileName, runs)
WordAnalyse(fileName, punctuation)
LetterAnalyse(fileName, punctuation)
LineAnalyse(fileName, punctuation)
