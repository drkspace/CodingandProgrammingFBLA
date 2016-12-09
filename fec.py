##############
#Daniel Kramer, Johns Creek High School
#Version 0.5.2
#2016-2017 FBLA Coding and Programming Competition
#https://github.com/drkspace/CodingandProgrammingFBLA
##############

#TODO Better Formatting
#TODO Allow selecting customer/employee from table to edit
#TODO Refined search in the tables
#TODO Allow sorting the tables

#Importing all from Tkinter
from Tkinter import *
import ttk
import Tkinter
import tkMessageBox
import tkFileDialog
import tkColorChooser

#Importing sqlite
import sqlite3

#Importing Random for Ids
import random 

#Importing config parser
import ConfigParser

#Version number
version = "0.5.2"

#Seting up config file parser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

#Getting the variables form the config
db_file=Config.get('DatabaseFile', 'Database')
row_Color_1 = Config.get('Colors', 'Row_1')
row_Color_2 = Config.get('Colors', 'Row_2')

#Setting up a connection to the sqlite database
conn = sqlite3.connect(db_file)

#Making a cursor to be able to manipulate the database
cur = conn.cursor()

#List of the days of the week for reference later in the program
day_week=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
day_week_short=['sun','mon','tues','wend','thurs','fri','sat']



#making a new window
window =Tk()

#setting the size and title
window.geometry("1000x500")
window.title("FEC")

#Used to make all the necessary tables in the database
#If the table already exist, nothing happens to that database here 
def create_table():

	#Create a table for the employee's names and is's
	cur.execute('CREATE TABLE IF NOT EXISTS employee(employee_id REAL, first_name TEXT, last_name TEXT)')

	#Create a table for the days the employee is working
	cur.execute('CREATE TABLE IF NOT EXISTS employee_schedule(employee_id REAL, sun_attend VALUE, mon_attend VALUE, tues_attend VALUE, wend_attend VALUE, thurs_attend VALUE, fri_attend VALUE, sat_attend VALUE)')

	#Create a table for the the customers names and id's 
	cur.execute('CREATE TABLE IF NOT EXISTS customer(customer_id REAL, first_name TEXT, last_name TEXT)')

	#Create a table for the times and days the customer attended
	#Key for day_attend
	#0 - Neither AM nor PM
	#1 - PM
	#2 - AM
	#3 - AM/PM
	cur.execute('CREATE TABLE IF NOT EXISTS customer_schedule(customer_id REAL, sun_attend REAL, mon_attend REAL, tues_attend REAL, wend_attend REAL, thurs_attend REAL, fri_attend REAL, sat_attend REAL)')

#Adds an employee to the database
def add_Employee_or_Customer_to_db(fName, lName, sun, mon, tues, wend, thur, fri, sat, type):

	#Generate a random Id for the employee
	rndID = random.randrange(0,10000000)
	
	#Test to see if the ID is already used with another employee
	while(True):

		#Tries to SELECT employees with the generated ID
		cur.execute('SELECT * FROM '+type+' WHERE '+type+'_id = '+str(rndID))
	
		#If there exist an employee with that id, generate another id
		if(len(cur.fetchall())!=0):
			rndID = random.randrange(0,10000000)
		
		#Break out of the loop if there were no matching id's found
		else:
			break

	#Insert the names and id into the employee table 
	cur.execute('INSERT INTO '+type+'('+type+'_id, first_name, last_name) VALUES(?,?,?)', (rndID,fName,lName))
	
	cur.execute('INSERT INTO '+type+'_schedule('+type+'_id, sun_attend, mon_attend, tues_attend, wend_attend, thurs_attend, fri_attend, sat_attend) VALUES(?,?,?,?,?,?,?,?)', (rndID,sun,mon,tues,wend,thur,fri,sat))
	
	#Commit the changes to save
	conn.commit()

def addEmployee():

	#Create a new frame for the modules to be put into and to be deleted later on
	frame=Frame(window)
	frame.grid(row = 0, column = 0)

	#Taking user input
	#New label for what the user is going to input
	label1=Label(frame, text="Employee's First Name")
	label1.grid(row=3, column=0)
	E=Entry(frame)
	E.grid(row=3, column=5)

	label2=Label(frame, text="Employee's Last Name")
	label2.grid(row=4, column=0)
	E1=Entry(frame)
	E1.grid(row=4, column=5)

	label3=Label(frame, text="Please select the days the employee is working:")
	label3.grid(row=5, column=0)
	
	#Creating a list for the variables from the buttons
	dayVar=[]
	for i in xrange(7):
		dayVar.append(IntVar())
	
	#Creating a list of buttons
	dayButtons=[]
	for i in xrange(7):
		
		#Filling the buttons with th days of the week and the corresponding variable
		dayButtons.append(Checkbutton(frame, text = day_week[i], variable = dayVar[i]))
	
	#Put all of the buttons on the grid
	for i in xrange(7):
		dayButtons[i].grid(row=7+i,column=0)

	#Adds a check all buttons
	#When the button is checked, calls the checkAll method and passes in the dayButtons list
	check_All=Checkbutton(frame, text = "Check All Boxes", command = lambda: checkAll(dayButtons, 0) )
	check_All.grid(row=6,column=0)

	#Method to delete the frame and return to the menu
	def runMenu():
		frame.grid_forget()
		menu()
	
	#Button to return to the menu
	toMenu=Button(frame, text="Back to the Menu", command=runMenu)
	toMenu.grid(row=7, column=5)

	#Method to store the variables in the sql database
	def getInput():
		add_Employee_or_Customer_to_db(E.get(), E1.get(), dayVar[0].get(), dayVar[1].get(), dayVar[2].get(), dayVar[3].get(), dayVar[4].get(), dayVar[5].get(), dayVar[6].get(), 'employee')
		frame.grid_forget()
		menu()
	#Button to submit the input
	submit = Button(frame,text="Submit", command=getInput)
	submit.grid(row=14, column=0)

def add_Customer():	
	
	#Create a new frame for the modules to be put into and to be deleted later on
	frame=Frame(window)
	frame.grid(row = 0, column = 0)
	
	#taking user input
	#New label for what the user is going to input
	label1=Label(frame, text="Customers's First Name")
	label1.grid(row=3, column=0)

	#Get user input
	E=Entry(frame)
	E.grid(row=3, column=5)

	label2=Label(frame, text="Customers's Last Name")
	label2.grid(row=4, column=0)
	E1=Entry(frame)
	E1.grid(row=4, column=5)
	
	label3=Label(frame, text="Please select the days and times the customer is present:")
	label3.grid(row=5, column=0)

	#List to store the vars for the buttons
	AMVar=[]
	PMVar=[]
	for i in xrange(7):
		AMVar.append(IntVar())
		PMVar.append(IntVar())

	
	#List of buttons for AM and PM selections
	AMButton=[]
	PMButton=[]
	for i in xrange(7):
		AMButton.append(Checkbutton(frame, text="AM", variable = AMVar[i], onvalue=2, offvalue=0))
		PMButton.append(Checkbutton(frame, text="PM", variable = PMVar[i]))
	
	#Put the buttons in the frame
	for i in xrange(7):
		AMButton[i].grid(row=7+i, column=1)
		PMButton[i].grid(row=7+i, column=3)	
	
	#Put labels for each day of the week
	for i in xrange(len(day_week)):
		dayLabel=Label(frame, text=day_week[i]+":")
		dayLabel.grid(row=6+i, column=0)

	#Adds a check all buttons
	#When the button is checked, calls the t method and passes in the tmp list
	check_All=Checkbutton(frame, text = "Check All Boxes", command = lambda: checkAll(AMButton+PMButton, 0) )
	check_All.grid(row=6,column=1)


	#Get the input from each button
	def get_Input():
		
		#Sum the button values to either 0,1,2,3
		totals=[]
		for i in xrange(7):
			totals.append(AMVar[i].get()+PMVar[i].get())
		frame.grid_forget()
		menu()

		#Use the method to add the customer to the database
		add_Employee_or_Customer_to_db(removeSpaces(E.get()), removeSpaces(E1.get()), totals[0], totals[1], totals[2], totals[3], totals[4], totals[5], totals[6], 'customer')

	#Method to delete the frame and return to the menu
	def runMenu():
		frame.grid_forget()
		menu()

	#Button to return to the menu
	toMenu=Button(frame, text="Back to the Menu", command=runMenu)
	toMenu.grid(row=7, column=5)
	
	#Button to get input from the buttons
	submit = Button(frame,text="submit", command=get_Input)
	submit.grid(row=14, column=0)

	#Method and button for displaying the attendance of the customers
	def show_customer_attendance():
		del_menu()
		print_Attendance_Customer()
	printCButton=Button(frame, text="Print Customer Attendance", command=show_customer_attendance)
	printCButton.grid(row=8, column=5)

#Method to set a customers attendance
def customer_attendance():

	#Creating a new frame to have all of the modules held in
	#To be deleted at the end of the method
	frame=Frame(window)
	frame.grid(row=0, column=0)

	#Label for the information on what the user has to input 
	label0=Label(frame, text='Please enter the customers name')
	label0.grid(row=0,column=0)
	label=Label(frame, text="Customer's First Name")
	label.grid(row=1, column=0)

	#Entry for the first name
	E=Entry(frame)
	E.grid(row=2, column=0)
	label1=Label(frame, text="Customer's Last Name")
	label1.grid(row=3, column=0)
	
	#Entry for the last name
	E1=Entry(frame)
	E1.grid(row=4, column=0)
	
	#Method for after the user submitted a name
	#Searches in the customer database 
	def edit():
		
		#Selects from the customer table if there is a matching first and last name
		cur.execute('SELECT * FROM customer WHERE last_name = ? AND first_name=?',(E1.get(),E.get()))
			
		#Stores the data in a list
		data=cur.fetchall()

		#Test to see if the array has data in it
		#If it has data, continue to let the user edit the data
		if(len(data)>0):

			#Remove the toSearch button
			toSearch.grid_forget()

			#Store the customers first and last name
			o_LN=E1.get()
			o_FN=E.get()

			#Display the old name to the user so they can remember
			#Use the old labels to save memory
			label0.configure(text="Please enter the new information")
			label.configure(text="Customer's first name: "+o_FN)
			label1.configure(text="Customer's last name: "+o_LN)

			#Remove the text entry from the frame
			E.grid_forget()
			E1.grid_forget()

			#Label to tell the user what he/she needs to input
			label3=Label(frame, text="Please select the days and times the customer is present:")
			label3.grid(row=5, column=0)


			#List of variables for the AM and PM buttons
			intVarListAM=[]
			intVarListPM=[]
			for i in xrange(7):
				intVarListAM.append(IntVar())
				intVarListPM.append(IntVar())
	
			
			#List of AM and PM Buttons
			AMButton=[]
			PMButton=[]
			for i in xrange(7):

				#Button for the AM selection
				#Has values of 0 and 2 for the way the time is stored in the database
				AMButton.append(Checkbutton(frame, text="AM", variable = intVarListAM[i], onvalue=2, offvalue=0))

				#Button for the PM
				PMButton.append(Checkbutton(frame, text="PM", variable = intVarListPM[i]))

			#Put all of the buttons on the grid
			for i in xrange(7):
				AMButton[i].grid(row=7+i, column=1)
				PMButton[i].grid(row=7+i, column=2)

			#Adds a check all buttons
			#When the button is checked, calls the t method and passes in the tmp list
			check_All=Checkbutton(frame, text = "Check All Boxes", command = lambda: checkAll(AMButton+PMButton, 0) )
			check_All.grid(row=6,column=1)

			#Store the customer id in id
			id=str(data[0][0])	

			#Selecting the data from customer attendance with the correct customer id
			cur.execute('SELECT * FROM customer_schedule WHERE customer_id = '+id)

			#Storing the attendance in attend
			attend = cur.fetchall()
			for i in attend:

				#Loop to have all of the buttons selected if they were selected before
				for k in xrange(8):
					if(i[k]>=4):
						continue
					if(i[k]==0):
						continue
					if(i[k]==1):
						PMButton[k-1].select()
					if(i[k]==2):
						AMButton[k-1].select()
					if(i[k]==3):
						AMButton[k-1].select()
						PMButton[k-1].select()

			#Display all of the days of the week
			for i in xrange(len(day_week)):
				dayLabel=Label(frame, text=day_week[i]+":")
				dayLabel.grid(row=6+i, column=0)
			
			#Method to store what the user has selected at that moment
			def get_input():
				
				
				#Add up each day total and store it in total
				total=[]
				for i in xrange(7):
					total.append(intVarListAM[i].get()+intVarListPM[i].get())
				for i in xrange(7):
					#Have to update each day's attendance individually, limitation in sqlite3
					cur.execute("UPDATE customer_schedule SET "+day_week_short[i]+"_attend = ? WHERE customer_id = ?",(str(total[i]),id))
				
				
				#Commit the changes
				conn.commit()

				#Delete the frame
				frame.grid_forget()

				#Run the menu
				menu()

			def delete_record():
				delete_from_Database(1,id)
				frame.grid_forget()
				menu()
			#Button to delete the person
			deleteButton = Button(frame, text='Delete Record', command = delete_record)
			deleteButton.grid(row=14, column=0)

			#Button to submit the changes
			submit = Button(frame,text="submit", command=get_input)
			submit.grid(row=15, column=0)

		#If there is no matching customers		
		else:
		
			#Creating a label explaining to the user that there was no matching name in the database
			errorLabel=Label(frame, text="Error finding the person you inputed, please check the name")
			errorLabel.grid(row=7, column=0)

	#Button to search within the database to find the person 
	toSearch = Button(frame, text='Search', command=edit)
	toSearch.grid(row=5, column=0)
	
	#Method to delete the frame and run the menu	
	def toMenu():
		frame.grid_forget()
		menu()

	#Button to get back to the menu
	toMenu = Button(frame, text='Back to the Menu', command=toMenu)
	toMenu.grid(row=4,column=1)

#Method to put all of the employees in a table on screen
def showAll_Employee():

	#Creating a new table
	tbl = ttk.Treeview()

	#Setting the column to be called firstName
	tbl['columns']=('firstName')	

	#Change the leading column to have the text "Last Name"
	tbl.heading('#0', text='Last Name')

	#Change the size of the leading column
	tbl.column('#0', anchor = 'center', width = 100)

	#Set the firstName column to show "First Name"
	tbl.heading('firstName', text='First Name')

	#Change the size of the firstName column
	tbl.column('firstName', anchor ='center', width = 100)

	#Put the table on the grid
	tbl.grid(row=5, column=0)

	#Select all of the first and last names form employee
	cur.execute('SELECT last_name, first_name FROM employee')

	#Make color assigner so each column would have alternating colors
	color_assigner=1

	#Loop for putting all of the names in the table
	for i in cur.fetchall():
		tbl.insert('', 'end', text=i[0], values=(i[1]),tags =(str(color_assigner,)))

		#Multiply the color assigner by -1 so it would alternate between -1 and 1
		color_assigner*=-1

	#Set the color of the columns depending on the color assigner
	tbl.tag_configure(str(1), background=row_Color_1)
	tbl.tag_configure(str(-1), background=row_Color_2)

	#Method to remove the table and go back to the menu
	def runMenu():
			tbl.grid_remove()
			toMenu.grid_remove()
			menu()

	#Button to go back to the menu
	toMenu=Button(window, text="Back to the Menu", command=runMenu)
	toMenu.grid(row=0, column=0)

#Method to show the attendance of the customers
def print_Attendance_Customer():

	#Making the table
	tbl = ttk.Treeview()

	#Setting the columns to the first/last name and the day of the week
	tbl['columns']=('firstName',day_week[0],day_week[1],day_week[2],day_week[3],day_week[4],day_week[5],day_week[6])
	
	#Setting the 1st column to have the name Last Name
	tbl.heading('#0', text='Last Name')

	#Setting the 1st column's size
	tbl.column('#0', anchor = 'center', width = 100)

	#Setting the 2nd column to have the name of First Name
	tbl.heading('firstName', text='First Name')

	#Setting the size of first name
	tbl.column('firstName', anchor ='center', width = 100)

	#Setting all of the other columns to show the day of the week
	for day in day_week:
		tbl.heading(day, text=day)
		
		#Meting the size of the column
		tbl.column(day, anchor='center', width = 75)

	#Putting the table on the grid
	tbl.grid(row=5,column=0																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																														)

	#Make color assigner so each column would have alternating colors
	color_assigner = 1

	#Selecting everything from customer attendance
	cur.execute('SELECT * FROM customer_schedule')

	#Storing the customer attendance in attendance
	attendance = cur.fetchall()
	for i in attendance:
		
		#Selecting the names of the customer with matching id numbers
		cur.execute('SELECT last_name, first_name FROM customer WHERE customer_id = '+str(i[0]))
		for k in cur.fetchall():

			#Having AMPM store what the certain cell of the table should display depending on the stored number
			AMPM=[]
			for j in i:
				if(j>=4):
					continue
				if(j==0):
					AMPM.append('Absent')
				if(j==1):
					AMPM.append('PM')
				if(j==2):
					AMPM.append('AM')
				if(j==3):
					AMPM.append('AM/PM')

			#Inserting the information into the table
			tbl.insert('', 'end', text=k[0], values=(k[1], AMPM[0], AMPM[1],AMPM[2],AMPM[3],AMPM[4],AMPM[5],AMPM[6]), tags =(str(color_assigner,)))	
			
			#Multiplying color assigner by -1 to have is cycle between -1 and 1
			color_assigner*=-1

		#Setting the background color depending on the color assigned
		tbl.tag_configure(str(1), background=row_Color_1)
		tbl.tag_configure(str(-1), background=row_Color_2)

	#Method to run the menu and delete the table
	def runMenu():
			tbl.grid_remove()
			toMenu.grid_remove()
			addCButton.grid_remove()
			menu()

	#Button to go back to the menu
	toMenu=Button(window, text="Back to the Menu", command=runMenu)
	toMenu.grid(row=0, column=0)

	#Method and button for adding an customer to the system
	def add_customer_():
		tbl.grid_remove()
		toMenu.grid_remove()
		addCButton.grid_remove()
		add_Customer()
	addCButton=Button(window, text="Add customers", command=add_customer_)
	addCButton.grid(row=2, column=0)

#Method to print the schedule of the employees
def print_Schedule_All():

	#Creating the table
	tbl = ttk.Treeview()

	#Setting the column names
	tbl['columns']=('firstName',day_week[0],day_week[1],day_week[2],day_week[3],day_week[4],day_week[5],day_week[6])
	
	#Setting the 1st column to display last name
	tbl.heading('#0', text='Last Name')

	#Setting the size of the first column
	tbl.column('#0', anchor = 'center', width = 100)

	#Setting the 2nd column to show "First Name"
	tbl.heading('firstName', text='First Name')

	#Setting the size of the second column
	tbl.column('firstName', anchor ='center', width = 100)

	#Setting all of the other columns to show the day of the week
	for day in day_week:
		tbl.heading(day, text=day)
		
		#Meting the size of the column
		tbl.column(day, anchor='center', width = 75)

	#Setting the position of the table
	tbl.grid(row=5, column=0)

	#Make color assigner so each column would have alternating colors
	color_assigner = 1

	#Selecting everything from the employee schedule
	cur.execute('SELECT * FROM employee_schedule')

	#Storing the selection to schedule
	schedule = cur.fetchall()

	#Method for changing the number stored for the correct word	
	def change_number_to_word(numlist):
	
		#Loop through the numlist	
		for i in xrange(len(numlist)):

			#change numlist to a tuple
			numlist=list(numlist)

			#If it is 0, change it to Absent
			if numlist[i]==0:
				numlist[i]="Absent"

			#If it is 1, change it to Present
			if numlist[i]==1:
				numlist[i]="Present"

		#Return the updates numlist
		return numlist	

	for i in schedule:

		#Change the numbers to words		
		i=change_number_to_word(i)

		#Selecting the first and last name with the matching employee id
		cur.execute('SELECT last_name, first_name FROM EMPLOYEE WHERE employee_id = '+str(i[0]))
		for k in cur.fetchall():

			#Writing the data to the table
			tbl.insert('', 'end', text=k[0], values=(k[1], i[1], i[2],i[3],i[4],i[5],i[6],i[7]), tags =(str(color_assigner,)))	
		
		#Multiply the color assigner by -1 so it would alternate between -1 and 1
		color_assigner*=-1

	#Set the color of the columns depending on the color assigner
	tbl.tag_configure(str(1), background= row_Color_1)
	tbl.tag_configure(str(-1), background= row_Color_2)

	#Method to remove the table and go back to the menu
	def runMenu():
			tbl.grid_remove()
			toMenu.grid_remove()
			menu()

	#Button to go back to the menu
	toMenu=Button(window, text="Back to the Menu", command=runMenu)
	toMenu.grid(row=0, column=0)

#Method to edit an employee
def edit_Employee():

	#Making the frame to have all of the modules put into it
	#To be deleted at the end of the method
	frame=Frame(window)
	frame.grid(row=0, column=0)
	
	#Setting the label to tell the user what to do
	label0=Label(frame, text='Please enter the old information')
	label0.grid(row=0,column=0)

	#Setting the label and input for the first name
	label=Label(frame, text="Employee's First Name")
	label.grid(row=1, column=0)
	E=Entry(frame)
	E.grid(row=2, column=0)

	#Setting the label and input for the last name
	label1=Label(frame, text="Employee's Last Name")
	label1.grid(row=3, column=0)
	E1=Entry(frame)
	E1.grid(row=4, column=0)
	
	#Method to goto the editing screen
	def edit():
		
		
		#Stores the old first and last name and removes the spaces form the users input
		o_LN=removeSpaces(E1.get())
		o_FN=removeSpaces(E.get())

		#Select the employee with the matching names
		cur.execute('SELECT * FROM employee WHERE last_name = ? AND first_name=?',(o_LN,o_FN))

		#Test to see if there is data in the selection
		tmp = cur.fetchall()
		if(len(tmp)>0):

			#Sets the id
			id = tmp[0][0]

			#Deletes the toSearch Button
			toSearch.grid_forget()

			#Ask the user for the new information
			#It uses the same input boxes as before so they have the old names already inputted
			label0.configure(text="Please enter the new information")
			label.configure(text="Employee's old first name: "+o_FN)
			label1.configure(text="Employee's old last name: "+o_LN)
			
			#Method for setting the first and last names in the database
			def get_input():
				LN=E1.get()

				#Use 2 different updates because of a limitation in sqlite3
				cur.execute('UPDATE employee SET last_name = ? WHERE last_name = ? AND first_name = ?',(removeSpaces(LN),o_LN,o_FN))
				cur.execute('UPDATE employee SET first_name = ? WHERE last_name = ? AND first_name = ?',(removeSpaces(E.get()),o_LN,o_FN))
				
				#Committing the changes
				conn.commit()

				#Deleting the frame
				frame.grid_forget()
	
				#Returning to the menu
				menu()

			
			def delete_record():
				delete_from_Database(0,id)
				frame.grid_forget()
				menu()
			#Button to delete the person
			deleteButton = Button(frame, text='Delete Record', command = delete_record)
			deleteButton.grid(row=14, column=0)

			#Button to submit the new information
			submit = Button(frame,text="submit", command=get_input)
			submit.grid(row=13, column=0)
	
	#Button to search with what the user has inputed
	toSearch = Button(frame, text='Search', command=edit)
	toSearch.grid(row=5, column=0)

	#Method to delete the frame and return to the menu
	def toMenu():
		frame.grid_forget()
		menu()
	
	#Button to return to the menu
	toMenu = Button(frame, text='Back to the Menu', command=toMenu)
	toMenu.grid(row=5,column=1)	

#Method to edit the employee's schedule
def edit_Employee_Schedule():

	#Frame to store all of the modules and to be deleted later on
	frame=Frame(window)
	frame.grid(row=0, column=0)

	#Label to ask the user for the name
	label0=Label(frame, text="Please enter the Employee's name that you want the schedule to be changed for.")
	label0.grid(row=0,column=0)

	#Setting the label and input for the first name
	label=Label(frame, text="Employee's First Name")
	label.grid(row=1, column=0)
	E=Entry(frame)
	E.grid(row=2, column=0)

	#Setting the label and input for the last name
	label1=Label(frame, text="Employee's Last Name")
	label1.grid(row=3, column=0)
	E1=Entry(frame)
	E1.grid(row=4, column=0)

	#Method for getting the input from the user
	def edit():
		
		#Finding the employee with the searched name
		cur.execute('SELECT * FROM employee WHERE last_name = ? AND first_name=?',(E1.get(),E.get()))
		data = cur.fetchall()

		#Test to see if there data in the selection
		if(len(data)>0):

			#Deletes the search button
			toSearch.grid_forget()

			#Stores the old last/first names
			o_LN=E1.get()
			o_FN=E.get()

			#Remove the search boxes
			E.grid_remove()
			E1.grid_remove()

			#Display the old first/last name
			label0.configure(text="Please enter the new information")
			label.configure(text="Employee's first name: "+o_FN)
			label1.configure(text="Employee's last name: "+o_LN)

			#Creating a list for the variables from the buttons
			dayVar=[]
			for i in xrange(7):
				dayVar.append(IntVar())

			#Creating a list of buttons
			dayButtons=[]
			for i in xrange(7):
		
				#Filling the buttons with th days of the week and the corresponding variable
				dayButtons.append(Checkbutton(frame, text = day_week[i], variable = dayVar[i]))
	
			#Put all of the buttons on the grid
			for i in xrange(7):
				dayButtons[i].grid(row=7+i,column=0)
		
			#Adds a check all buttons
			#When the button is checked, calls the checkAll method and passes in the dayButtons list
			check_All=Checkbutton(frame, text = "Check All Boxes", command = lambda: checkAll(dayButtons, 0) )
			check_All.grid(row=6,column=0)

			for i in data:

				#Selecting the data from the schedule with the correct id
				cur.execute('SELECT * FROM employee_schedule WHERE employee_id='+ str(i[0]))
				for j in cur.fetchall():

					#Loop to have all of the buttons selected if they were selected before
					for k in xrange(7):

						#Test to see if the value isn't a valid value
						if(j[k]>=4):
							continue
						if(j[k]==0):
							continue
						if(j[k]==1):
							dayButtons[k-1].select()
				
				#Method for editing the schedule and going back to the menu
										
				def get_input():
					#dayButtons_var=[]
					#for i in xrange(7):
						#dayButtons_var.append(dayVar[i].get())
					edit_schedule(i[0], dayVar)
					frame.grid_forget()
					menu()
			
				#Button to submit the schedule and go back to the menu
				submit = Button(frame,text="submit", command=get_input)
				submit.grid(row=14, column=0)
					
	#Button to search with the given name	
	toSearch = Button(frame, text='Search', command=edit)
	toSearch.grid(row=5, column=0)	

	#Method to go back to the menu 
	def toMenu():
		frame.grid_forget()
		menu()

	#Button to go back to the menu
	toMenu = Button(frame, text='Back to the Menu', command=toMenu)
	toMenu.grid(row=5,column=1)

#Method to delete an employee/customer from their database
#If dbType is 0 - Employee
#If dbType is 1 - Customer
def delete_from_Database(dbType, Id):

	#Changes the int to the coresponding string
	db = ""
	if dbType == 0:
		db = "employee"
	elif dbType == 1:
		db = "customer"
	else:
		print "There as been an error, invalid dbType"
		return

	#Delete the row in the databases with the matching id
	cur.execute('DELETE FROM '+db+' WHERE '+db+'_id = '+str(Id))
	cur.execute('DELETE FROM '+db+'_schedule WHERE '+db+'_id = '+str(Id))
	conn.commit()

#Method for editing the schedule
def edit_schedule(eId, attend_list):

	for i in xrange(len(attend_list)):
		#Have to call separate UPDATE commands because of a limitation in sqlite3
		cur.execute('UPDATE employee_schedule SET '+day_week_short[i]+'_attend= ? WHERE employee_id= ?',(str(attend_list[i].get()),eId))
	

	#Committing the change to save it
	conn.commit()

#Method to run the menu	
def menu():

	#Label to welcome the user to the system
	#Put in the label not in the frame but in the window so it can be centers over the buttons
	welcomeLabel=Label(window, text="Welcome to the Family Entertainment System")
	welcomeLabel.grid(row=0,column=0)

	#Frame to hold all the modules and to be deleted later
	frame = Frame(window)
	frame.grid(row=1, column=0)

	#Method to delete the frame and the welcome label
	def del_menu():
		frame.grid_forget()
		welcomeLabel.grid_forget()

	#Method and button for adding an employee to the system
	def addButtonCommandAndRemove():
		del_menu()
		addEmployee()
	addButton = Button(frame, text="Add Employee", command=addButtonCommandAndRemove)
	addButton.grid(row=1,column=0)

	#Method and button for showing all the employees in the system
	def showButtonCommandAndRemove():
		del_menu()
		showAll_Employee()					
	showButton = Button(frame, text="Show all Employees", command=showButtonCommandAndRemove)
	showButton.grid(row=2,column=0)
	
	#Method and button for printing the employee schedule
	def print_Schedule():
		del_menu()
		print_Schedule_All()
	schedButton = Button(frame, text="Print Weekly Schedule", command=print_Schedule)
	schedButton.grid(row=3, column=0)

	#Method and button for editing an employees information
	def edit_Employee_Run():
		del_menu()
		edit_Employee()
	editButton = Button(frame, text ="Edit/Delete an Employee's details", command = edit_Employee_Run)
	editButton.grid(row=4, column =0)
		
	#Method and button for editing an employees work schedule
	def edit_Employee_Schedule_Run():
		del_menu()
		edit_Employee_Schedule()
	editSButton = Button(frame, text ="Edit an Employee's Schedule details", command = edit_Employee_Schedule_Run)
	editSButton.grid(row=5, column =0)

	#Method and button for adding an customer to the system
	def add_customer_():
		del_menu()
		add_Customer()
	addCButton=Button(frame, text="Add customers", command=add_customer_)
	addCButton.grid(row=1, column=2)
	
	#Method and button for editing a customers attendance
	def edit_Customer_attednace():
		del_menu()
		customer_attendance()
	editCButton=Button(frame, text="Change/Delete Customers Information", command=edit_Customer_attednace)
	editCButton.grid(row=2, column=2)

	#Method and button for displaying the attendance of the customers
	def show_customer_attendance():
		del_menu()
		print_Attendance_Customer()
	printCButton=Button(frame, text="Print Customer Attendance", command=show_customer_attendance)
	printCButton.grid(row=3, column=2)

#Method for displaying the help box
def help():
	win=Tk()
	win.geometry("300x250")
	win.title("Help")
	text=Text(win)
	text.insert(INSERT, "Press one of the Buttons to goto that\ndesired section\n\nUse the options in file to open/save a\ndatabase\n\nUse the options menu to change the colors of the tables\n\n")
	text.pack()

#Method for displaying the information about the program
def info():
	win=Tk()
	win.geometry("202x200")
	win.title("Info")
	text=Text(win)
	text.insert(INSERT, "Created by Daniel Kramer for the 2016-2017 FBLA Coding & Programming competition.\n\nVersion "+version)
	text.pack()

#Method to allow the user to save a file
def save_file():
		
	#Opening a box for a user entering a new save file
	f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".db")

	#If the user leaves the box w/o entering a file
	if f is None:
		return

	#Open the file and copy it to a string
	with open(db_file) as myfile:
  		data=myfile.read()

	#Write the old file to the new location
	f.write(data)

	#Closes the location pointer
	f.close()

#Method to open a file
#No checking to see if the file is in the right format
def open_file():
	
	#Opens a open box
	db_file = tkFileDialog.askopenfilename()

	#If the user preses cancel
	if db_file is None:
		return

	#sets conn to the global variable and changes the connection location to that file
	global conn
	conn=sqlite3.connect(db_file)

	#sets conn to the global variable and changes the connection location to that file
	global cur
	cur=conn.cursor()
	
	#Save the new database file to the config file
	cfgfile = open("config.ini",'w')
	Config.set('DatabaseFile', 'Database', db_file)
	Config.write(cfgfile)
	cfgfile.close()
	
#Method for making a new database
def new_database():

	#Creating name for new database
	db_file="Untitled.db"

	#sets conn to the global variable and changes the connection location to that file
	global conn
	conn=sqlite3.connect(db_file)

	#sets conn to the global variable and changes the connection location to that file
	global cur
	cur=conn.cursor()

	create_table()

#Helper method that removes spaces before and/or after strings
def removeSpaces(string):

	#Converting the string passed in to a char list
	sList = list(string)

	#Checks to see if the first character is a space
	if(sList[0]==' '):
		del sList[0]

	#Checks to see if the last character is a space
	if(sList[len(sList)-1]==' '):
		del sList[len(sList)-1]

	#Makes the list into a string and returns it
	string = ''.join(sList)
	return string

#Method that checks all checkboxes in a list of buttons
#if mode is 0 -> select all buttons
#if mode is 1 -> deselect all buttons
def checkAll(list_of_checkbox, mode):

	#Loop through the list
	for i in xrange(len(list_of_checkbox)):
		if(mode==0):
			list_of_checkbox[i].select()
		if(mode==1):
			list_of_checkbox[i].deselect()

#Method to change the color of the rows in the charts
#Gets the old color passed in
#Gets row color var number passed in
def Change_chart_color(color,var):

	#Call the tkColorChooser which opens a popup box with a color slider
	color_result=tkColorChooser.askcolor(color, title="Please Pick a new Color")

	#Test to see if the user press cancel
	#If true, return out of the method
	if color_result == (None,None):
		return

	#Converts the rgb returned by the color chooser and converts it into the hex code
	color_result_hex= '#%02x%02x%02x' % (color_result[0][0],color_result[0][1],color_result[0][2])

	#Test from the var to see what row color needs to be changed
	if var == 1:
		global row_Color_1
		row_Color_1=color_result_hex

		#Save the new database file to the config file
		cfgfile = open("config.ini",'w')
		Config.set('Colors', 'Row_1', row_Color_1)
		Config.write(cfgfile)
		cfgfile.close()
	elif var == 2: 
		global row_Color_2
		row_Color_2=color_result_hex

		#Save the new database file to the config file
		cfgfile = open("config.ini",'w')
		Config.set('Colors', 'Row_2', row_Color_2)
		Config.write(cfgfile)
		cfgfile.close()
	else:
		return
		
#Creating the menu at the top
menubar = Menu(window)
helpmenu = Menu(menubar, tearoff=0)
filemenu = Menu(menubar, tearoff=0)
options = Menu(menubar, tearoff=0)
color_options=Menu()

#Adding all of the menu options
helpmenu.add_command(label="Help", command=help)
helpmenu.add_command(label="Info", command=info)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="New", command=new_database)
options.add_cascade(label="Change chart color", menu=color_options)
color_options.add_command(label="Change Color 1", command = lambda: Change_chart_color(row_Color_1,1))
color_options.add_command(label="Change Color 2", command = lambda: Change_chart_color(row_Color_2,2))

#Creating the help and file cascade
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Options", menu=options)
menubar.add_cascade(label="Help", menu=helpmenu)
window.config(menu=menubar)

#To make the tables if they are not present
create_table()

#Starting the menu
menu()

#starting the window
window.mainloop()


