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

