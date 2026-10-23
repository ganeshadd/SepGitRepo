#Lower case Func
def process_lower(ganesh):
    print("I am in process of lower block")
    lowerCase =ganesh.lower()
    return lowerCase

#Open the File
# C:\Users\ganes\SeptDemo\input.txt
# input.txt
file =open("input.txt","r")

#Read the file
content =file.read()

#print the content

result =process_lower(content)
print(result)

