# Functions Demo

#Define variable
FirstName ="Ganesh"
LastName="Adabala"
sessionNo ="9"

# Define Function
def calculateCost(sessionNo):
    SessionCost =10
    TrainingCost = sessionNo*SessionCost
    return TrainingCost

def fullName(fName,lName):
    output = fName+lName
    return output

# Execute the function
Result =calculateCost(sessionNo)
Result2=fullName(FirstName,sessionNo)

#Print the result
print(Result2)