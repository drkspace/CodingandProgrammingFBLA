class customer(object):

	def __init__(self):
		pass

	def add_Customer():

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
			menu()

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

