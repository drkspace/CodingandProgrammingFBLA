from random import randrange
from fec_global_variables import cur


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

            
