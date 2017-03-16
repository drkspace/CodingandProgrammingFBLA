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
    

            
