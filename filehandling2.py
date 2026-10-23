#Lower case Func
def process_lower(ganesh):
    print("I am in process of lower block.")
    lowerCase =ganesh.lower()
    return lowerCase

file_name =input("Enter the file name you want to process:: ")
with open(file_name,"r") as file:
    print("I am reading ",file_name)
    content =file.read()
result =process_lower(content)
print(result)
