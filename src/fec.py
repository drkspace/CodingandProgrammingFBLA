#######################################
#Daniel Kramer, Johns Creek High School
#Version 0.6.0
#2016-2017 FBLA Coding and Programming Competition
#https://github.com/drkspace/CodingandProgrammingFBLA
#######################################

#TODO Make better looking
#TODO Allow selecting customer/employee from table to edit
#TODO Refined search in the tables
#TODO Allow sorting the tables

from sys import exit

try:
	#Importing all the variables and methods
	from fec_global_variables import *
	from fec_helper_methods import *
	from customer import _customer
	from employee import _employee
	
except Exception as e:
	print str(e)
	print "Please re-download the program from https://github.com/drkspace/CodingandProgrammingFBLA"
	print "Please don't delete any of the downloaded files or else the program won't work"
	exit(0)

try:
	#Importing all from Tkinter
	from Tkinter import *
	import tkFileDialog
	import tkColorChooser

	#Importing sqlite
	import sqlite3

	#Importing Random for Ids
	import random

	#Importing config parser
	import ConfigParser

	#Importing to call terminal commands
	from subprocess import call
	from shutil import copyfile

except:
	print "Please Run the executable version located at https://github.com/drkspace/CodingandProgrammingFBLA/releases"
	print "or please download the following modules:\nTkinter\nsqlite3\nrandom\nConfigParser\nsubprocess\nshutil"
	exit(0)

#Version number
version = "0.6.0"

#Used to make all the necessary tables in the database
#If the table already exist, nothing happens to that database here
#This is to be ran first
def create_table():

	#Create a table for the employee's names and id's
	cur.execute('CREATE TABLE IF NOT EXISTS employee(employee_id REAL, first_name TEXT, last_name TEXT)')

	#Create a table for the days the employee is working
	cur.execute('CREATE TABLE IF NOT EXISTS employee_schedule(employee_id REAL, sun_attend VALUE, mon_attend VALUE, tues_attend VALUE, wend_attend VALUE, thurs_attend VALUE, fri_attend VALUE, sat_attend VALUE)')

	#Create a table for the the customers names and id's
	cur.execute('CREATE TABLE IF NOT EXISTS customer(customer_id REAL, first_name TEXT, last_name TEXT)')

	#Create a table for the times and days the customer attended
	#Only required to store if the customer is attending in the am or pm
	#Key for day_attend
	#0 - Neither AM nor PM
	#1 - PM
	#2 - AM
	#3 - AM/PM
	cur.execute('CREATE TABLE IF NOT EXISTS customer_schedule(customer_id REAL, sun_attend REAL, mon_attend REAL, tues_attend REAL, wend_attend REAL, thurs_attend REAL, fri_attend REAL, sat_attend REAL)')

#Method to assist the recreation of the menu
def menu_helper(amethod):
	run_menu.set(False)
	amethod()
	window.wait_variable(run_menu)
	menu()

#Method to run the menu
def menu():

	#Creating an employee and customer object
	employee = _employee()
	customer = _customer()

	#Label to welcome the user to the system
	#Put in the label not in the frame but in the window so it can be centers over the buttons
	welcomeLabel = Label(window, text="Welcome to the Family Entertainment System")
	welcomeLabel.grid(row=0, column=0, sticky='w')

	#Frame to hold all the modules and to be deleted later
	frame = Frame(window)
	frame.grid(row=1, column=0, sticky='w')

	#Method to delete the frame and the welcome label
	def del_menu():
		frame.grid_forget()
		welcomeLabel.grid_forget()

	#Method and button for adding an employee to the system
	def addButtonCommandAndRemove():
		del_menu()
		employee.addEmployee()
	addButton = Button(frame, text="Add Employee", command = lambda: menu_helper(addButtonCommandAndRemove))
	addButton.grid(row=1, column=0, sticky='w')

	#Method and button for showing all the employees in the system
	def showButtonCommandAndRemove():
		del_menu()
		employee.showAll_Employee()
	showButton = Button(frame, text="Show all Employees", command = lambda: menu_helper(showButtonCommandAndRemove))
	showButton.grid(row=2, column=0, sticky='w')

	#Method and button for printing the employee schedule
	def print_Schedule():
		del_menu()
		employee.print_Schedule_All()
	schedButton = Button(frame, text="Print Weekly Schedule", command = lambda: menu_helper(print_Schedule))
	schedButton.grid(row=3, column=0, sticky='w')

	#Method and button for editing an employees information
	def edit_Employee_Run():
		del_menu()
		employee.edit_Employee()
	editButton = Button(frame, text="Edit/Delete an Employee's details", command = lambda: menu_helper(edit_Employee_Run))
	editButton.grid(row=4, column=0, sticky='w')

	#Method and button for editing an employees work schedule
	def edit_Employee_Schedule_Run():
		del_menu()
		employee.edit_Employee_Schedule()
	editSButton = Button(frame, text="Edit an Employee's Schedule details", command = lambda: menu_helper(edit_Employee_Schedule_Run))
	editSButton.grid(row=5, column=0, sticky='w')

	#Method and button for adding an customer to the system
	def add_customer_():
		del_menu()
		customer.add_Customer()
	addCButton = Button(frame, text="Add customers", command = lambda: menu_helper(add_customer_))
	addCButton.grid(row=1, column=2, sticky='w')

	#Method and button for editing a customers attendance
	def edit_Customer_attednace():
		del_menu()
		customer.customer_attendance()
	editCButton = Button(frame, text="Change/Delete Customers Information", command = lambda: menu_helper(edit_Customer_attednace))
	editCButton.grid(row=2, column=2, sticky='w')

	#Method and button for displaying the attendance of the customers
	def show_customer_attendance():
		del_menu()
		customer.print_Attendance_Customer()
	printCButton = Button(frame, text="Print Customer Attendance", command = lambda: menu_helper(show_customer_attendance))
	printCButton.grid(row=3, column=2, sticky='w')

#Method for displaying the help box
def help():
	win = Tk()
	win.geometry("300x250")
	win.title("Help")
	text = Text(win)
	text.insert(INSERT, "Press one of the Buttons to goto that\ndesired section\n\nUse the options in file to open/save a\ndatabase\n\nUse the options menu to change the colors of the tables\n\n")
	text.pack()

#Method for displaying the information about the program
def info():
	win = Tk()
	win.geometry("202x200")
	win.title("Info")
	text = Text(win)
	text.insert(INSERT, "Created by Daniel Kramer for the 2016-2017 FBLA Coding & Programming competition.\n\nVersion "+version)
	text.pack()

#Method to allow the user to save a file
def save_file():

	#Opening a box for a user entering a new save file
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".db")

	#If the user leaves the box w/o entering a file
    if f is None:
        return

    if os == 'Linux':
        call(['cp', db_file ,  f.name])
        return
    elif os == 'Windows':
        copyfile(db_file, f.name)
        return
        

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
    conn = sqlite3.connect(db_file)

    #sets conn to the global variable and changes the connection location to that file
    global cur
    cur = conn.cursor()

    #Save the new database file to the config file
    cfgfile = open("config.ini", 'w')
    Config.set('DatabaseFile', 'Database', db_file)
    Config.write(cfgfile)
    cfgfile.close()

#Initialization for the program    
def __init__():
    #Creating the menu at the top
    menubar = Menu(window)
    helpmenu = Menu(menubar, tearoff=0)
    filemenu = Menu(menubar, tearoff=0)
    options = Menu(menubar, tearoff=0)
    color_options = Menu()

    #Adding all of the menu options
    helpmenu.add_command(label="Help", command=help)
    helpmenu.add_command(label="Info", command=info)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Open", command=open_file)
    #filemenu.add_command(label="", command=new_database)
    options.add_cascade(label="Change chart color", menu=color_options)
    color_options.add_command(label="Change Color 1", command=lambda: Change_chart_color(row_Color_1, 1))
    color_options.add_command(label="Change Color 2", command=lambda: Change_chart_color(row_Color_2, 2))

    #Creating the help and file cascade
    menubar.add_cascade(label="File", menu = filemenu)
    menubar.add_cascade(label="Options", menu = options)
    menubar.add_cascade(label="Help", menu = helpmenu)
    window.config(menu = menubar)

#Main program loop
def main():

    #To make the tables if they are not present
    create_table()

    #Starting the menu
    menu()

    #starting the window
    window.mainloop()

#Starting the program
if __name__=='__main__':
    __init__()
    main()
