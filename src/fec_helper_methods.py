#(c)Daniel Robert Kramer,2017. All Rights Reseved
from random import randrange
from fec_global_variables import cur, run_menu, window, conn, color, stheme, Config, row_Color_1, row_Color_2
from Tkinter import Button, Checkbutton, Entry, Label
import tkColorChooser
import ttk
import random
import colors
import copy

#Helper method that removes spaces before and/or after strings
def removeSpaces(string):

	#Converting the string passed in to a char list
	sList = list(string)

	if len(sList) is 0:
		return " "

	#Checks to see if the first character is a space
	if(sList[0] == ' '):
		del sList[0]

	#Checks to see if the last character is a space
	if(sList[len(sList)-1] == ' '):
		del sList[len(sList)-1]

	#Makes the list into a string and returns it
	string = ''.join(sList)
	return string

def switch_slash(string):

    #Converting the string passed in to a char list
    sList = list(string)

    #Looping through the char list
    for i in range(len(sList)):

        #Switching if the is a / or \
        if sList[i]=='/':
            sList[i]='\\'
            continue
        elif sList[i]=='\\':
            sList[i]='/'
            continue

    #Returning the string
    return ''.join(sList)


#Adds an employee or customer to the database
def add_to_db(fName, lName, sun, mon, tues, wend, thur, fri, sat, type):

	#Generate a random Id for the employee
	rndID = random.randrange(0, 10000000)

	#Test to see if the ID is already used with another employee
	while(True):

		#Tries to SELECT employees with the generated ID
		cur.execute('SELECT * FROM '+type+' WHERE '+type+'_id = '+str(rndID))

		#If there exist an employee with that id, generate another id
		if(len(cur.fetchall()) != 0):
			rndID = random.randrange(0, 10000000)

		#Break out of the loop if there were no matching id's found
		else:
			break

	#Insert the names and id into the employee table
	#cur.execute('INSERT INTO '+type+'('+type+'_id, first_name, last_name) VALUES(?,?,?)', (rndID, fName, lName))

	cur.execute('INSERT INTO '+type+'('+type+'_id , first_name, last_name, sun_attend, mon_attend, tues_attend, wend_attend, thurs_attend, fri_attend, sat_attend) VALUES(?,?,?,?,?,?,?,?,?,?)', (rndID, fName, lName, sun, mon, tues, wend, thur, fri, sat))

	#Commit the changes to save
	conn.commit()

#Method to delete the frame and return to the menu
def runMenu(frame):
    frame.grid_forget()
    run_menu.set(True)
    return

#Method to change the color of the rows in the charts
#Gets the old color passed in
#Gets row color var number passed in
def Change_chart_color(color, var):

	#Call the tkColorChooser which opens a popup box with a color slider
	color_result = tkColorChooser.askcolor(color, title="Please Pick a new Color")

	#Test to see if the user press cancel
	#If true, return out of the method
	if color_result == (None, None):
		return

	#Converts the rgb returned by the color chooser and converts it into the hex code
	color_result_hex = '#%02x%02x%02x' % (color_result[0][0], color_result[0][1], color_result[0][2])

	cfgfile = open("config.ini", 'w')
	#Test from the var to see what row color needs to be changed
	if var == 1:
	
		#Save the new color to the config file
		Config.set('Colors', 'Row_1', color_result_hex)
	elif var == 2:
	
		#Save the new color to the config file
		Config.set('Colors', 'Row_2', color_result_hex)
	else:
		cfgfile.close()
		return
		
	Config.write(cfgfile)
	cfgfile.close()
	
	global row_Color_1
	global row_Color_2
	row_Color_1 = Config.get('Colors', 'Row_1')
	row_Color_2 = Config.get('Colors', 'Row_2')


#Method that checks all checkboxes in a list of buttons
#if mode is 0 -> select all buttons
#if mode is 1 -> deselect all buttons
def checkAll(list_of_checkbox, mode):

	#Loop through the list
	for i in xrange(len(list_of_checkbox)):

		if(mode == 0):
			list_of_checkbox[i].select()
		if(mode == 1):
			list_of_checkbox[i].deselect()

#Method to delete an employee/customer from their database
def delete_from_Database(dbType, Id):

	#Checks to see if the passed in database type is valid
	if dbType not in ['employee', 'customer']:
		print("There has been an error, invalid dbType")
		return

	#Delete the row in the databases with the matching id
	
	cur.execute('DELETE FROM {} WHERE {}_id = ?'.format(dbType,dbType), (Id,))
	conn.commit()

def change_color_palet(widget_list, atheme=stheme, changewindow=True):

	global color
	tmpColor = copy.copy(color)

	if atheme is not stheme:
		tmpColor.set_color_theme(atheme)

	if changewindow==True:
		window.configure(background=tmpColor.background)

	for i in widget_list:

		if isinstance(i,Button):
			i.configure(highlightbackground=tmpColor.accent, background=tmpColor.background, foreground=tmpColor.text_color)

		elif isinstance(i,Checkbutton):
			i.configure(highlightbackground=tmpColor.background, foreground=tmpColor.text_color, background=tmpColor.background)

		elif isinstance(i,Entry):
			i.configure(highlightbackground=tmpColor.accent, background=tmpColor.entry, fg = tmpColor.text_color)

		elif isinstance(i,ttk.Treeview):
			ttk.Style().configure("Treeview", fieldbackground=tmpColor.table_background)

		elif isinstance(i,Label):
			i.configure(foreground=tmpColor.text_color, background=tmpColor.background)

		else:
			i.configure(background=tmpColor.background)

def format_enum_name(astr):
	alist=list(astr)
	for i in range(len(alist)):
		if i == 0 or (i is not 0 and alist[i-1] is " "):
			alist[i]=alist[i].capitalize()
		if alist[i] is "_":
			alist[i]=" "
	return ''.join(alist)

