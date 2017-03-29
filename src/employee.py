from fec_global_variables import *

class employee(object):

	def __init__(self):
		pass


	def addEmployee():

		#Create a new frame for the modules to be put into and to be deleted later on
		frame = Frame(window)
		frame.grid(row=0, column=0, sticky='w')

		#Taking user input
		#New label for what the user is going to input
		label1 = Label(frame, text="Employee's First Name")
		label1.grid(row=3, column=0, sticky='w')
		E = Entry(frame)
		E.grid(row=3, column=5, sticky='w')

		label2 = Label(frame, text="Employee's Last Name")
		label2.grid(row=4, column=0, sticky='w')
		E1 = Entry(frame)
		E1.grid(row=4, column=5, sticky='w')

		label3 = Label(frame, text="Please select the days the employee is working:")
		label3.grid(row=5, column=0,columnspan=2, sticky='w')

		#Creating a list for the variables from the buttons
		dayVar = []
		for i in xrange(7):
			dayVar.append(IntVar())

		#Creating a list of buttons
		dayButtons = []
		for i in xrange(7):

			#Filling the buttons with th days of the week and the corresponding variable
			dayButtons.append(Checkbutton(frame, text=day_week[i], variable=dayVar[i]))

		#Put all of the buttons on the grid
		for i in xrange(7):
			dayButtons[i].grid(row=7+i, column=0, sticky='w')

		#Adds a check all buttons
		#When the button is checked, calls the checkAll method and passes in the dayButtons list
		check_All = Checkbutton(frame, text="Check All Boxes", command = lambda: checkAll(dayButtons, 0))
		check_All.grid(row=6, column=0, sticky='w')

		#Button to return to the menu
		toMenu = Button(frame, text="Back to the Menu", command = lambda: runMenu(frame))
		toMenu.grid(row=7, column=5, sticky='w')

		#Method to store the variables in the sql database
		def getInput():
			add_to_db(E.get(), E1.get(), dayVar[0].get(), dayVar[1].get(), dayVar[2].get(), dayVar[3].get(), dayVar[4].get(), dayVar[5].get(), dayVar[6].get(), 'employee')
			runMenu(frame)
		#Button to submit the input
		submit = Button(frame, text="Submit", command=getInput)
		submit.grid(row=14, column=0, sticky='w')

	#Method to put all of the employees in a table on screen
	def showAll_Employee():

            #Creating a new table
            tbl = ttk.Treeview()

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

            #Select all of the first and last names form employee
            cur.execute('SELECT last_name, first_name FROM employee')

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
                return selectedItem() is not None:

            #Returns the selection if there is a selection
            def getSelected(): 
                 if isSelected():
                        return selectedItem()
                 else:
                        return None

            label_notify=Label(window,  text="The employee has been removed, please refresh the table")
            #Return the Id for the selection
            def getID():
                employee  = getSelected()
                val = employee['values']
                f_name = val[0]
                cur.execute('SELECT * FROM employee WHERE last_name = ? AND first_name = ?', (employee['text'], f_name))
                for i in cur.fetchall():
                    label_notify.grid(row=3, column=0, sticky='w')
                    return i[0]


            deleteEmployeeButton = Button(window,  text = "Delete This Employee",  command = lambda: delete_from_Database('employee', getID()))
            deleteEmployeeButton.grid(row=2, column=2, sticky='w')    

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
                addEmployee()

            #Button to add an employee
            addEmployeeButton = Button(text="Add employee",  command = add_employee)
            addEmployeeButton.grid(row=2, column=3, sticky='w')

                #Method to remove the table and go back to the menu
            def runMenu():
                    del_cur_frame()
                    menu()

            #Button to go back to the menu
            toMenu = Button(window, text="Back to the Menu", command=runMenu)
            toMenu.grid(row=0, column=0, sticky='w')



