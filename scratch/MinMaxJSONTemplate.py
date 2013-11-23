#Converting between CSV and JSON file formats with Python

#Why do we care about this?
#All of our D2 data is in .csv format, but it's sometimes easier to work with 
#JSON when using d3

#first we import the csv and json libraries
import csv
import json

#we open the csv file that we want to convert to JSON.It has to be in the same
#folder as this python file.
# 'rb' means we'll be reading it
ourcsv = open( 'costsdept.csv', 'rb' )


#then we run the csv.DictReader method on our csv file
#this method creates a dictionary, which is pretty much the format we need
#for JSON - {"fieldname1":value1a, "fieldname2":value2a}, {"fieldname1":value1b
#"fieldname2":value2b} etc
#the fieldnames are taken from the first line of the csv file if there is a
#header, OR we can specify them, as we have done below
dict = csv.DictReader(ourcsv, fieldnames = ["PolicyName", "Department", "mincost", "maxcost"])

#we can check to see if this is what we want (though right now I have it commen
#ted out)
#for row in dict:
#   print(row)

#we see that our values only have single quotes. Apparently for JSON it's very 
#important  (from reading a D3 tutorial) that they have double quotes. 

#So we'll have to use a JSON method, dumps. dumps formats a series of dictionar
#y entries into a JSON entry (JSON format has no line breaks). 

out = json.dumps( [row for row in dict] )

#the cheap and cheerful method here is to print our JSON formatted "out" 
#to copy the printed output into a text file and save with the extension .JSON,
# which is what I have done successfully
print(out)



#I can't quite figure out how to save it directly using a python script.
#You'll note that numeric values have double quotes. Once in d3 it is pretty
#simple to edit these fields using (using parseInt( ) or parseFloat()) to turn
#them into numbers
