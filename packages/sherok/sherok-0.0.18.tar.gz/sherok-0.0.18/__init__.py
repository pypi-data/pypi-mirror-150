import pyttsx3
import random
import webbrowser
import sys
import time
import pyjokes
import requests
import randfacts

def add2nums(num1, num2):
    return num1 + num2

def sub2nums(num1, num2):
    return num1 - num2

def mul2nums(num1, num2):
    return num1 * num2

def div2nums(num1, num2):
    return num1 / num2

def webopen(link):
    webbrowser.open(link)

def wait(sec):
    time.sleep(sec)

def ask(inputtext):
    input(inputtext)

def pr(txt):
    print(txt)

def pstop():
    sys.exit()

def talk(txt):
    robo = pyttsx3.init()
    robo.say(txt)
    robo.runAndWait()

def rickroll():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def joke():
    r = requests.get('https://sv443.net/jokeapi/v2/joke/Miscellaneous,Pun,Spooky,Christmas?blacklistFlags=nsfw,racist,sexist&type=single').json()
    joke = r['joke']
    return joke

def pjoke():
    joke = pyjokes.get_joke()
    return joke

def fact():
    f = randfacts.get_fact()
    return f

def ranum(upto):
    num = random.randrange(upto)
    return num

def open_yt():
    webbrowser.open("https://youtube.com")

def open_google():
    webbrowser.open("https://google.com")

def open_newtab():
    webbrowser.open_new_tab()