from fec_global_variables import *
import ttk

class _customer(object):

	def __init__(self):
		pass

	def add_Customer(self):

		#Create a new frame for the modules to be put into and to be deleted later on
		frame = Frame(window)
		frame.grid(row=0, column=0, sticky='w')

		#taking user input
			#New label for what the user is going to input
		label1 = Label(frame, text="Customers's First Name")
		label1.grid(row=3, column=0, sticky='w')

		#Get user input
		E = Entry(frame)
		E.grid(row=3, column=5, sticky='w')

		label2 = Label(frame, text="Customers's Last Name")
		label2.grid(row=4, column=0, sticky='w')
		E1 = Entry(frame)
		E1.grid(row=4, column=5, sticky='w')

		label3 = Label(frame, text="Please select the days and times the customer is present:")
		label3.grid(row=5, column=0,columnspan=4, sticky='w')

		#List to store the vars for the buttons
		AMVar = []
		PMVar = []
		for i in xrange(7):
			AMVar.append(IntVar())
			PMVar.append(IntVar())

		#List of buttons for AM and PM selections
		AMButton = []
		PMButton = []
		for i in xrange(7):

			#Have the on value set to two for parsing if it was selected later
			AMButton.append(Checkbutton(frame, text="AM", variable=AMVar[i], onvalue=2, offvalue=0))
			PMButton.append(Checkbutton(frame, text="PM", variable=PMVar[i]))

		#Put the buttons in the frame
		for i in xrange(7):
			AMButton[i].grid(row=7+i, column=1, sticky='w')
			PMButton[i].grid(row=7+i, column=3, sticky='w')

		#Put labels for each day of the week
		for i in xrange(len(day_week)):
			dayLabel = Label(frame, text=day_week[i]+":")
			dayLabel.grid(row=7+i, column=0, sticky='w')

		#Adds a check all buttons
		#When the button is checked, calls the t method and passes in the tmp list
		check_All = Checkbutton(frame, text="Check All Boxes", command=lambda: checkAll(AMButton+PMButton, 0))
		check_All.grid(row=6, column=1, sticky='w')

		#Get the input from each button
		def get_Input():

			#Sum the button values to either 0,1,2,3
			totals = []
			for i in xrange(7):
				totals.append(AMVar[i].get()+PMVar[i].get())
			frame.grid_forget()
			run_menu.set(True)
		    	return

			#Use the method to add the customer to the database
			add_to_db(removeSpaces(E.get()), removeSpaces(E1.get()), totals[0], totals[1], totals[2], totals[3], totals[4], totals[5], totals[6], 'customer')

		#Button to return to the menu
		toMenu = Button(frame, text="Back to the Menu", command=lambda: runMenu(frame))
		toMenu.grid(row=7, column=5, sticky='w')

		#Button to get input from the buttons
		submit = Button(frame, text="submit", command=get_Input)
		submit.grid(row=14, column=0, sticky='w')

		#Method and button for displaying the attendance of the customers
		def show_customer_attendance():
			del_menu()
			print_Attendance_Customer()
		printCButton = Button(frame, text="Print Customer Attendance", command=show_customer_attendance)
		printCButton.grid(row=8, column=5, sticky='w')

	#Method to set a customers attendance
	def customer_attendance(self):

		#Creating a new frame to have all of the modules held in
		#To be deleted at the end of the method
		frame = Frame(window)
		frame.grid(row=0, column=0, sticky='w')

		#Label for the information on what the user has to input
		label0 = Label(frame, text='Please enter the customers name')
		label0.grid(row=0, column=0, sticky='w')
		label = Label(frame, text="Customer's First Name")
		label.grid(row=1, column=0, sticky='w')

		#Entry for the first name
		fName_Entry = Entry(frame)
		fName_Entry.grid(row=2, column=0, sticky='w')
		label1 = Label(frame, text="Customer's Last Name")
		label1.grid(row=3, column=0, sticky='w')

		#Entry for the last name
		lName_Entry = Entry(frame)
		lName_Entry.grid(row=4, column=0, sticky='w')

		#Method for after the user submitted a name
		#Searches in the customer database
		def edit():

			#Selects from the customer table if there is a matching first and last name
			cur.execute('SELECT * FROM customer WHERE last_name = ? AND first_name=?', (lName_Entry.get(), fName_Entry.get()))

			#Stores the data in a list
			data = cur.fetchall()

			#Test to see if the array has data in it
			#If it has data, continue to let the user edit the data
			if(len(data) > 0):

				#Remove the toSearch button
				toSearch.grid_forget()

				#Store the customers first and last name
				old_LN = lName_Entry.get()
				old_FN = fName_Entry.get()

				#Display the old name to the user so they can remember
				#Use the old labels to save memory
				label0.configure(text="Please enter the new information")
				label.configure(text="Customer's first name: "+old_FN)
				label1.configure(text="Customer's last name: "+old_LN)

				#Remove the text entry from the frame
				fName_Entry.grid_forget()
				lName_Entry.grid_forget()

				#Label to tell the user what he/she needs to input
				label3 = Label(frame, text="Please select the days and times the customer is present:")
				label3.grid(row=5, column=0, sticky='w')

				#List of variables for the AM and PM buttons
				intVarListAM = []
				intVarListPM = []
				for i in xrange(7):
					intVarListAM.append(IntVar())
					intVarListPM.append(IntVar())

				#List of AM and PM Buttons
				AMButton = []
				PMButton = []
				for i in xrange(7):

					#Button for the AM selection
					#Has values of 0 and 2 for the way the time is stored in the database
					AMButton.append(Checkbutton(frame, text="AM", variable=intVarListAM[i], onvalue=2, offvalue=0))

					#Button for the PM
					PMButton.append(Checkbutton(frame, text="PM", variable=intVarListPM[i]))

				#Put all of the buttons on the grid
				for i in xrange(7):
					AMButton[i].grid(row=7+i, column=1, sticky='w')
					PMButton[i].grid(row=7+i, column=2, sticky='w')

				#Adds a check all buttons
				#When the button is checked, calls the t method and passes in the tmp list
				check_All = Checkbutton(frame, text="Check All Boxes", command=lambda: checkAll(AMButton+PMButton, 0))
				check_All.grid(row=6, column=1, sticky='w')

				#Store the customer id in id
				id = str(data[0][0])

				#Selecting the data from customer attendance with the correct customer id
				cur.execute('SELECT * FROM customer_schedule WHERE customer_id = '+id)

				#Storing the attendance in attend
				attend = cur.fetchall()
				for i in attend:

					#Loop to have all of the buttons selected if they were selected before
					for k in xrange(8):
						if(i[k] >= 4):
							continue
						if(i[k] == 0):
							continue
						if(i[k] == 1):
							PMButton[k-1].select()
						if(i[k] == 2):
							AMButton[k-1].select()
						if(i[k] == 3):
							AMButton[k-1].select()
							PMButton[k-1].select()

				#Display all of the days of the week
				for i in xrange(len(day_week)):
					dayLabel = Label(frame, text=day_week[i]+":")
					dayLabel.grid(row=6+i, column=0, sticky='w')

				#Method to store what the user has selected at that moment
				def get_input():

					#Add up each day total and store it in total
					total = []
					for i in xrange(7):
						total.append(intVarListAM[i].get()+intVarListPM[i].get())
					for i in xrange(7):
						#Have to update each day's attendance individually, limitation in sqlite3
						cur.execute("UPDATE customer_schedule SET "+day_week_short[i]+"_attend = ? WHERE customer_id = ?", (str(total[i]), id))

					#Commit the changes
					conn.commit()

					#Run the menu and delet the frame
					runMenu(frame)

				def delete_record():
					delete_from_Database('customer', id)

					#Run the menu and delet the frame
					runMenu(frame)
				#Button to delete the person
				deleteButton = Button(frame, text='Delete Record', command=delete_record)
				deleteButton.grid(row=14, column=0, sticky='w')

				#Button to submit the changes
				submit = Button(frame, text="submit", command=get_input)
				submit.grid(row=15, column=0, sticky='w')

			#If there is no matching customers
			else:

				#Creating a label explaining to the user that there was no matching name in the database
				errorLabel = Label(frame, text="Unable to find the person you inputed, please check the name again")
				errorLabel.grid(row=7, column=0, sticky='w',columnspan=3)

		#Button to search within the database to find the person
		toSearch = Button(frame, text='Search', command=edit)
		toSearch.grid(row=5, column=0, sticky='w')

		#Button to get back to the menu
		toMenu = Button(frame, text='Back to the Menu', command = lambda: runMenu(frame))
		toMenu.grid(row=4, column=1, sticky='w')
	

	#Method to show the attendance of the customers
	def print_Attendance_Customer(self):

	    #Making the table
	    tbl = ttk.Treeview()

	    #Setting the columns to the first/last name and the day of the week
	    tbl['columns'] = ('firstName', day_week[0], day_week[1], day_week[2], day_week[3], day_week[4], day_week[5], day_week[6])

	    #Setting the 1st column to have the name Last Name
	    tbl.heading('#0', text='Last Name')

	    #Setting the 1st column's size
	    tbl.column('#0', anchor='center', width=100)

	    #Setting the 2nd column to have the name of First Name
	    tbl.heading('firstName', text='First Name')

	    #Setting the size of first name
	    tbl.column('firstName', anchor='center', width=100)

	    #Putting the table on the grid
	    tbl.grid(row=2, column=0, sticky='w')	

	    #Setting all of the other columns to show the day of the week
	    for day in day_week:
		tbl.heading(day, text=day)

		#Meting the size of the column
		tbl.column(day, anchor='center', width=75)

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
		    AMPM = []
		    for j in i:
		        if(j >= 4):
		            continue
		        if(j == 0):
		            AMPM.append('Absent')
		        if(j == 1):
		            AMPM.append('PM')
		        if(j == 2):
		            AMPM.append('AM')
		        if(j == 3):
		            AMPM.append('AM/PM')

		    #Inserting the information into the table
		    tbl.insert('', 'end', text=k[0], values=(k[1], AMPM[0], AMPM[1], AMPM[2], AMPM[3], AMPM[4], AMPM[5], AMPM[6]), tags =(str(color_assigner,)))

		    #Multiplying color assigner by -1 to have is cycle between -1 and 1
		    color_assigner *= -1

		#Setting the background color depending on the color assigned
		tbl.tag_configure(str(1), background=row_Color_1)
		tbl.tag_configure(str(-1), background=row_Color_2)

	    #Return the selected item from the table
	    def selectedItem(): 
		curItem = tbl.focus()
		return tbl.item(curItem)

	    #Test to see if there is an item selected    
	    def isSelected():
		return selectedItem() is not None

	    #Return the employee info is there is a selection
	    def getSelected(): 
		if isSelected():
		    customer = selectedItem()
		    return customer
		else:
		    return None
	    label_notify=Label(window,  text="The customer has been deleted")
	    #Return the Id of the employee
	    def getID():
		customer  = getSelected()
		val = customer['values']
		f_name = val[0]
		cur.execute('SELECT * FROM customer WHERE last_name = ? AND first_name = ?', (customer['text'], f_name))
		for i in cur.fetchall():
		    label_notify.grid(row=3,  column = 2, sticky='w')
		    return i[0]

	    deleteEmployeeButton = Button(window,  text = "Delete This Customer",  command = lambda: delete_from_Database('customer', getID()) )
	    deleteEmployeeButton.grid(row=2, column=2, sticky='w')

	    #Method to run the menu and delete the table
	    def runMenu():
		    deleteEmployeeButton.grid_remove()

		    label_notify.grid_remove()
		    tbl.grid_remove()
		    toMenu.grid_remove()
		    addCButton.grid_remove()
		    run_menu.set(True)
		    return

	    #Button to go back to the menu
	    toMenu = Button(window, text="Back to the Menu", command=runMenu)
	    toMenu.grid(row=0, column=0, sticky='w')

	    #Method and button for adding an customer to the system
	    def add_customer_():
		tbl.grid_remove()
		toMenu.grid_remove()
		addCButton.grid_remove()
		deleteEmployeeButton.grid_remove()
		add_Customer()

	    addCButton = Button(window, text="Add customers", command=add_customer_)
	    addCButton.grid(row=2, column=3, sticky='w')

