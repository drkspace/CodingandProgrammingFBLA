from random import randrange
from fec_global_variables import cur, run_menu

#Helper method that removes spaces before and/or after strings
def removeSpaces(string):

	#Converting the string passed in to a char list
	sList = list(string)

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
	cur.execute('INSERT INTO '+type+'('+type+'_id, first_name, last_name) VALUES(?,?,?)', (rndID, fName, lName))

	cur.execute('INSERT INTO '+type+'_schedule('+type+'_id, sun_attend, mon_attend, tues_attend, wend_attend, thurs_attend, fri_attend, sat_attend) VALUES(?,?,?,?,?,?,?,?)', (rndID, sun, mon, tues, wend, thur, fri, sat))

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

	#Test from the var to see what row color needs to be changed
	if var == 1:
		global row_Color_1
		row_Color_1 = color_result_hex

		#Save the new database file to the config file
		cfgfile = open("config.ini", 'w')
		Config.set('Colors', 'Row_1', row_Color_1)
		Config.write(cfgfile)
		cfgfile.close()
	elif var == 2:
		global row_Color_2
		row_Color_2 = color_result_hex

		#Save the new database file to the config file
		cfgfile = open("config.ini", 'w')
		Config.set('Colors', 'Row_2', row_Color_2)
		Config.write(cfgfile)
		cfgfile.close()
	else:
		return

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
#If dbType is 0 - Employee
#If dbType is 1 - Customer
def delete_from_Database(dbType, Id):

	#Changes the int to the corresponding string
	if dbType not in ['employee', 'customer']:
		print("There has been an error, invalid dbType")
		return

	#Delete the row in the databases with the matching id
	cur.execute('DELETE FROM '+dbType+' WHERE '+dbType+'_id = '+str(Id))
	cur.execute('DELETE FROM '+dbType+'_schedule WHERE '+dbType+'_id = '+str(Id))
	conn.commit()


