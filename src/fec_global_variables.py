#(c)Daniel Robert Kramer,2017. All Rights Reseved

#Importing config parser
import ConfigParser
#Importing sqlite
import sqlite3
#Importing all from Tkinter
from Tkinter import *
from tkFont import Font

#Import platfrom to get the os type
import platform

import colors

#Setting the platform
os = platform.system()

#Version number
version = "1.0.0"

#Setting up config file parser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

#Getting the variables form the config
db_file = Config.get('DatabaseFile', 'Database')
row_Color_1 = Config.get('Colors', 'Row_1')
row_Color_2 = Config.get('Colors', 'Row_2')
stheme = Config.get('Colors', 'theme')
stheme = colors.theme[stheme]
color = colors.colors()
color.set_color_theme(stheme)

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
window.geometry("950x500")
window.title("Our Family Center for Entertainment")

#Variable to signal when to open the menu
run_menu=BooleanVar()

#List of curent widgets
widgets=[]

#Title font
title = Font(size=25, weight="bold")
