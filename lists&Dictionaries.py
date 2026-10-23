# List

Persons =["Srini","ganesh",15 ,32.6,True]

print(Persons[0])

# Dictionaries

user1 = {
    "Name":"Ganesh","Course":"GenAi","Exp":15
}
users = [{
    "Name":"Ganesh","Course":"GenAi","Exp":12
}
,{
    "Name":"Srini", "Course":"GenAi","Exp":18
},
{
    "Name":"Sarath", "Course":"GenAi","Exp":14
}
]
print(users[2]["Exp"])

# Conditions & loops

for i in users:
    if i["Exp"]>=15:  #True
        print(i["Name"], "above 15 years exp")
    else:
        print (i["Name"],"does not have experience above 15")

