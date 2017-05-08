#(c)Daniel Robert Kramer,2017. All Rights Reseved
from fec_global_variables import *
from fec_helper_methods import *
import ttk

class _employee(object):

	def addEmployee(self):

		#Create a new frame for the modules to be put into and to be deleted later on
		frame = Frame(window)
		frame.grid(row=0, column=0, sticky='w')
		widgets.append(frame)

		#Taking user input
		#New label for what the user is going to input
		label1 = Label(frame, text="Employee's First Name")
		label1.grid(row=3, column=0, sticky='w')
		widgets.append(label1)

		first_name = Entry(frame)
		first_name.grid(row=3, column=5, sticky='w')
		widgets.append(first_name)

		label2 = Label(frame, text="Employee's Last Name")
		label2.grid(row=4, column=0, sticky='w')
		widgets.append(label2)

		last_name = Entry(frame)
		last_name.grid(row=4, column=5, sticky='w')
		widgets.append(last_name)

		label3 = Label(frame, text="Please select the days the employee is working:")
		label3.grid(row=5, column=0,columnspan=100, sticky='w')
		widgets.append(label3)

		#Creating a list for the variables from the buttons
		#Filling the list with Tkinters IntVar()
		dayVar = [IntVar() for i in range(7)]

		#Creating a list of buttons
		#Filling the buttons with the days of the week and the corresponding variable
		dayButtons = [Checkbutton(frame, text=day_week[i], variable=dayVar[i]) for i in range(7)]

		#Put all of the buttons on the grid
		for i in range(7):
			dayButtons[i].grid(row=7+i, column=0, sticky='w')
			widgets.append(dayButtons[i])

		#Adds a check all buttons
		#When the button is checked, calls the checkAll method and passes in the dayButtons list
		check_All = Checkbutton(frame, text="Check All Boxes", command = lambda: checkAll(dayButtons, 0))
		check_All.grid(row=6, column=0, sticky='w')
		widgets.append(check_All)

		#Button to return to the menu
		toMenu = Button(frame, text="Back to the Menu", command = lambda: runMenu(frame))
		toMenu.grid(row=7, column=5, sticky='w')
		widgets.append(toMenu)

		#Method to store the variables in the sql database
		def getInput():
			add_to_db(first_name.get(), last_name.get(), dayVar[0].get(), dayVar[1].get(), dayVar[2].get(), dayVar[3].get(), dayVar[4].get(), dayVar[5].get(), dayVar[6].get(), 'employee')
			runMenu(frame)

		#Button to submit the input
		submit = Button(frame, text="Submit", command=getInput)
		submit.grid(row=14, column=0, sticky='w')
		widgets.append(submit)
		
		change_color_palet(widgets)
	
	#Method to put all of the employees in a table on screen
	def showAll_Employee(self):
	
            #Creating a new table
            tbl = ttk.Treeview()
	    widgets.append(tbl)

            #Setting the column to be called firstName
            tbl['columns'] = ('firstName')

            #Change the leading column to have the text "Last Name"
            tbl.heading('#0', text='Last Name')

            #Change the size of the leading column
            tbl.column('#0', anchor='center', width=100)

            #Set the firstName column to show "First Name"
            tbl.heading('firstName', text='First Name')

            #Change the size of the firstName column
            tbl.column('firstName', anchor='center', width=100)

            #Put the table on the grid
            tbl.grid(row=2, column=0, sticky='w')

            #Select all of the first and last names form employee and sort it
            cur.execute('SELECT last_name, first_name FROM employee ORDER BY last_name ASC')

            #Make color assigner so each column would have alternating colors
            color_assigner = 1

            #Loop for putting all of the names in the table
            for i in cur.fetchall():
                tbl.insert('', 'end', text=i[0], values=(i[1]), tags =(str(color_assigner,)))

                #Multiply the color assigner by -1 so it would alternate between -1 and 1
                color_assigner *= -1

            #Set the color of the columns depending on the color assigner
            tbl.tag_configure(str(1), background=row_Color_1)
            tbl.tag_configure(str(-1), background=row_Color_2)

            #Return the selected item from the table
            def selectedItem():
                curItem = tbl.focus()
                return tbl.item(curItem)

            #Test to see if there is an item selected    
            def isSelected():
                return selectedItem() is not None

            #Returns the selection if there is a selection
            def getSelected(): 
                 if isSelected():
                        return selectedItem()
                 else:
                        return None

            label_notify=Label(window,  text="The employee has been removed, please refresh the table")
	    widgets.append(label_notify)

            #Return the Id for the selection
            def getID():
                employee  = getSelected()
                val = employee['values']
                f_name = val[0]
                cur.execute('SELECT * FROM employee WHERE last_name = ? AND first_name = ? ', (employee['text'], f_name))
                for i in cur.fetchall():
                    label_notify.grid(row=3, column=0, sticky='w')
                    return i[0]

	    def reload(t='employee'):
		delete_from_Database(t, getID())
		del_cur_frame()
		self.showAll_Employee()

            deleteEmployeeButton = Button(window,  text = "Delete This Employee",  command = reload)
            deleteEmployeeButton.grid(row=0, column=1, sticky='w') 
	    widgets.append(deleteEmployeeButton)   

            #Method to delete all the items in the frame
            def del_cur_frame():
                label_notify.grid_remove()
                tbl.grid_remove()
                toMenu.grid_remove()
                deleteEmployeeButton.grid_remove()
                #editEmployeeButton.grid_remove()
                addEmployeeButton.grid_remove()

            #Method to goto the editing of the employee from the selection
            def edit_employee_(id):
                del_cur_frame()
                edit_employee_from_id(id)

            #Method to add an employee to the database from the table
            def add_employee():
                del_cur_frame()
                self.addEmployee()

            #Button to add an employee
            addEmployeeButton = Button(text="Add employee",  command = add_employee)
            addEmployeeButton.grid(row=0, column=2, sticky='w')
	    widgets.append(addEmployeeButton)

                #Method to remove the table and go back to the menu
            def runMenu():
                    del_cur_frame()
		    run_menu.set(True)
		    return

            #Button to go back to the menu
            toMenu = Button(window, text="Back to the Menu", command=runMenu)
            toMenu.grid(row=0, column=0, sticky='w')
	    widgets.append(toMenu)

	    change_color_palet(widgets)
	#Method to print the schedule of the employees
	def print_Schedule_All(self):

	    #Creating the table
	    tbl = ttk.Treeview()
	    widgets.append(tbl)

	    #Setting the column names
	    tbl['columns'] = ('firstName', day_week[0], day_week[1], day_week[2], day_week[3], day_week[4], day_week[5], day_week[6])

	    #Setting the 1st column to display last name
	    tbl.heading('#0', text='Last Name')

	    #Setting the size of the first column
	    tbl.column('#0', anchor='center', width=100)

	    #Setting the 2nd column to show "First Name"
	    tbl.heading('firstName', text='First Name')

	    #Setting the size of the second column
	    tbl.column('firstName', anchor='center', width=100)

	    #Setting all of the other columns to show the day of the week
	    for day in day_week:
		tbl.heading(day, text=day)

		#Meting the size of the column
		tbl.column(day, anchor='center', width=80)

	    #Setting the position of the table
	    tbl.grid(row=2, column=0, sticky='w')

	    #Make color assigner so each column would have alternating colors
	    color_assigner = 1

	    #Selecting everything from the employee schedule
	    cur.execute('SELECT * FROM employee ORDER BY last_name ASC')

	    #Storing the selection to schedule
	    schedule = cur.fetchall()

	    #Method for changing the number stored for the correct word
	    def change_number_to_word(numlist):

		#Loop through the numlist
		for i in range(len(numlist)):

		    #change numlist to a tuple
		    numlist = list(numlist)

		    #If it is 0, change it to Absent
		    if numlist[i] == 0:
		        numlist[i] = "Absent"

		    #If it is 1, change it to Present
		    if numlist[i] == 1:
		        numlist[i] = "Present"

		#Return the updates numlist
		return numlist

	    for i in schedule:

		#Change the numbers to words
		i = change_number_to_word(i)

		#Writing the data to the table
		tbl.insert('', 'end', text=i[1], values=(i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]), tags =(str(color_assigner,)))

		#Multiply the color assigner by -1 so it would alternate between -1 and 1
		color_assigner *= -1

	    #Set the color of the columns depending on the color assigner
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
		    employee = selectedItem()
		    return employee
		else:
		    return None

	    #Return the Id of the employee
	    def getID():
		employee  = getSelected()
		val = employee['values']
		f_name = val[0]
		cur.execute('SELECT * FROM employee WHERE last_name = ? AND first_name = ?', (employee['text'], f_name))
		for i in cur.fetchall():
		    return i[0]

	    def reload(t='employee'):
		delete_from_Database(t, getID())
		del_cur_frame()
		self.print_Schedule_All()

	    deleteEmployeeButton = Button(window,  text = "Delete This Employee",  command = lambda: delete_from_Database('employee', getID()) )
	    deleteEmployeeButton.grid(row=2, column=2, sticky='w')  
	    widgets.append(deleteEmployeeButton)  

	    def del_cur_frame():
		tbl.grid_remove()
		toMenu.grid_remove()
		deleteEmployeeButton.grid_remove()
		addEmployeeButton.grid_remove()

	    #Method to add an employee to the database from the table
	    def add_employee():
		del_cur_frame()
		self.addEmployee()

	    #Button to add an employee
	    addEmployeeButton = Button(text="Add employee",  command = lambda: self.add_employee())
	    addEmployeeButton.grid(row=2, column=3, sticky='w')
	    widgets.append(addEmployeeButton)

	    #Method to remove the table and go back to the menu
	    def runMenu():
		    del_cur_frame()
		    run_menu.set(True)
		    return

	    #Button to go back to the menu
	    toMenu = Button(window, text = "Back to the Menu", command=runMenu)
	    toMenu.grid(row=0, column=0, sticky='w')
	    widgets.append(toMenu)

	    change_color_palet(widgets)

	#Method to edit an employee
	def edit_Employee(self):

	    #Making the frame to have all of the modules put into it
	    #To be deleted at the end of the method
	    frame = Frame(window)
	    frame.grid(row=0, column=0, sticky='w')
	    widgets.append(frame)

	    #Setting the label to tell the user what to do
	    label0 = Label(frame, text='Please enter the old information')
	    label0.grid(row=0, column=0, sticky='w')
	    widgets.append(label0)

	    #Setting the label and input for the first name
	    label = Label(frame, text="Employee's First Name")
	    label.grid(row=1, column=0, sticky='w')
	    widgets.append(label)

	    fName_Entry = Entry(frame)
	    fName_Entry.grid(row=2, column=0, sticky='w')
	    widgets.append(fName_Entry)

	    #Setting the label and input for the last name
	    label1 = Label(frame, text="Employee's Last Name")
	    label1.grid(row=3, column=0, sticky='w')
	    widgets.append(label1)

	    lName_Entry = Entry(frame)
	    lName_Entry.grid(row=4, column=0, sticky='w')
	    widgets.append(lName_Entry)

	    #Method to goto the editing screen
	    def edit():

		#Stores the old first and last name and removes the spaces form the users input
		old_LN = removeSpaces(lName_Entry.get())
		old_FN = removeSpaces(fName_Entry.get())

		#Select the employee with the matching names
		cur.execute('SELECT * FROM employee WHERE last_name = ? AND first_name=?', (old_LN, old_FN))

		#Test to see if there is data in the selection
		tmp = cur.fetchall()
		if(len(tmp) > 0):

		    #Sets the id
		    eid = str(tmp[0][0])

		    #Deletes the toSearch Button
		    toSearch.grid_forget()

		    #Ask the user for the new information
		    #It uses the same input boxes as before so they have the old names already inputted
		    label0.configure(text="Please enter the new information")
		    label.configure(text="Employee's old first name: "+old_FN)
		    label1.configure(text="Employee's old last name: "+old_LN)

		    #Method for setting the first and last names in the database
		    def get_input():
		        LN = lName_Entry.get()
		        FN = fName_Entry.get()

			#Use 2 different updates because of a limitation in sqlite3
		        cur.execute('UPDATE employee SET last_name = ? WHERE employee_id = ?', (removeSpaces(LN), eid))
		        conn.commit()

		        cur.execute('UPDATE employee SET first_name = ? WHERE employee_id = ?', (removeSpaces(FN), eid))

			#Committing the changes
		        conn.commit()

			#Deleting the frame
		        frame.grid_forget()

			#Returning to the menu
		        run_menu.set(True)
		    	return

		    #Button to submit the new information
		    submit = Button(frame, text="submit", command=get_input)
		    submit.grid(row=13, column=0, sticky='w')
		    widgets.append(submit)

		    def delete_record():
		        delete_from_Database('employee', id)
		        frame.grid_forget()
		        run_menu.set(True)
		   	return

		    #Button to delete the person
		    deleteButton = Button(frame, text='Delete Record', command=delete_record)
		    deleteButton.grid(row=14, column=0, sticky='w')
		    widgets.append(deleteButton)

		change_color_palet(widgets)
	    #Button to search with what the user has inputed
	    toSearch = Button(frame, text='Search', command=edit)
	    toSearch.grid(row=5, column=0, sticky='w')
	    widgets.append(toSearch)

	    #Button to return to the menu
	    toMenu = Button(frame, text='Back to the Menu', command=lambda: runMenu(frame))
	    toMenu.grid(row=5, column=1, sticky='w')
	    widgets.append(toMenu)

	    change_color_palet(widgets)

	#Method to edit the employee's schedule
	def edit_Employee_Schedule(self):
		
		#Frame to store all of the modules and to be deleted later on
		frame = Frame(window)
		frame.grid(row=0, column=0, sticky='w')
		widgets.append(frame)

		#Label to ask the user for the name
		label0 = Label(frame, text="Please enter the Employee's name that you want the schedule to be changed for.")
		label0.grid(row=0, column=0,columnspan=100, sticky='w')
		widgets.append(label0)

		#Setting the label and input for the first name
		label = Label(frame, text="Employee's First Name")
		label.grid(row=1, column=0, sticky='w')
		widgets.append(label)

		first_name = Entry(frame)
		first_name.grid(row=2, column=0, sticky='w')
		widgets.append(first_name)

		#Setting the label and input for the last name
		label1 = Label(frame, text="Employee's Last Name")
		label1.grid(row=3, column=0, sticky='w')
		widgets.append(label1)
	
		last_name = Entry(frame)
		last_name.grid(row=4, column=0, sticky='w')
		widgets.append(last_name)

		#Method for getting the input from the user
		def edit():

			#widgets=[]		

			#Finding the employee with the searched name
			cur.execute('SELECT * FROM employee WHERE last_name = ? AND first_name=?', (last_name.get(), first_name.get()))
			data = cur.fetchall()

			#Test to see if there data in the selection
			if(len(data) > 0):

				#Deletes the search button
				toSearch.grid_forget()

				#Stores the old last/first names
				o_LN = last_name.get()
				o_FN = first_name.get()

				#Remove the search boxes
				first_name.grid_remove()
				last_name.grid_remove()

				#Display the old first/last name
				label0.configure(text="Please enter the new information")
				label.configure(text="Employee's first name: "+o_FN)
				label1.configure(text="Employee's last name: "+o_LN)

				#Creating a list for the variables from the buttons
				#Filling the list with Tkinters IntVar()
				dayVar = [IntVar() for i in range(7)]

				#Creating a list of buttons
				#Filling the buttons with the days of the week and the corresponding variable
				dayButtons = [Checkbutton(frame, text=day_week[i], variable=dayVar[i]) for i in range(7)]

				#Put all of the buttons on the grid
				for i in range(7):
					dayButtons[i].grid(row=7+i, column=0, sticky='w')
					widgets.append(dayButtons[i])
					

				#Adds a check all buttons
				#When the button is checked, calls the checkAll method and passes in the dayButtons list
				check_All = Checkbutton(frame, text="Check All Boxes", command=lambda: checkAll(dayButtons, 0))
				check_All.grid(row=6, column=0, sticky='w')
				widgets.append(check_All)

				for i in data:

					#Selecting the data from the schedule with the correct id
					cur.execute('SELECT * FROM employee WHERE employee_id=' + str(i[0]))
					for j in cur.fetchall():
						
						#Loop to have all of the buttons selected if they were selected before
						for k in xrange(3,10):
							
							#Test to see if the value isn't a valid value
							if(j[k] >= 4):
								continue
							elif(j[k] == 0):
								continue
							elif(j[k] == 1):
								dayButtons[k-3].select()

					#Method for editing the schedule and going back to the menu

					def get_input():
						dayButtons_var=[]
						for k in xrange(7):
							dayButtons_var.append(dayVar[k].get())
						self.edit_schedule(i[0], dayVar)
						frame.grid_forget()
						run_menu.set(True)
		   				return

					#Button to submit the schedule and go back to the menu
					submit = Button(frame, text="submit", command=get_input)
					submit.grid(row=14, column=0, sticky='w')
					widgets.append(submit)
	
					change_color_palet(widgets)

		#Button to search with the given name
		toSearch = Button(frame, text='Search', command=edit)
		toSearch.grid(row=5, column=0, sticky='w')
		widgets.append(toSearch)

		#Button to go back to the menu
		toMenu = Button(frame, text='Back to the Menu', command=lambda: runMenu(frame))
		toMenu.grid(row=5, column=1, sticky='w')	
		widgets.append(toMenu)

		change_color_palet(widgets)

	#Method for editing the schedule
	def edit_schedule(self, eId, attend_list):

		for i in xrange(len(attend_list)):

			#Have to call separate UPDATE commands because of a limitation in sqlite3
			cur.execute('UPDATE employee SET '+day_week_short[i]+'_attend= ? WHERE employee_id= ?', (str(attend_list[i].get()), eId))

		#Committing the change to save it
		conn.commit()

