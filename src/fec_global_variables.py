#Importing config parser
import ConfigParser
#Importing sqlite
import sqlite3
#Importing all from Tkinter
from Tkinter import *

#Import platfrom to get the os type
import platform

#Setting the platform
os = platform.system()

#Setting up config file parser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

#Getting the variables form the config
db_file = Config.get('DatabaseFile', 'Database')
row_Color_1 = Config.get('Colors', 'Row_1')
row_Color_2 = Config.get('Colors', 'Row_2')

#Setting up a connection to the sqlite database
conn = sqlite3.connect(db_file)

#Making a cursor to be able to manipulate the database
cur = conn.cursor()

#List of the days of the week for reference later in the program
day_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
day_week_short = ['sun', 'mon', 'tues', 'wend', 'thurs', 'fri', 'sat']

#making a new window
window = Tk()

#setting the size and title
window.geometry("1000x500")
window.title("Our Family Center for Entertainment")

run_menu=BooleanVar()
