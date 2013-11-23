
#Starting with the simulation.csv file, create a .json file for all 
#simulation parameters that contains as fields the following: parameter name, 
#department, whether-high-is-good (a value of 0 or 1).



#Import csv and JSON libraries
import csv
import sys
import json
#read from simulation.csv file
sim = open('simulation.csv', 'rb')

#with the file open, run csv reader method to parse the file and split at commas
csvsim = csv.reader(sim)

#open new csv file to write to
simdept = open('simdept.csv', 'wb')

#run csv writer method to allow us write rows
newfile = csv.writer(simdept)

#ignore headers
csvsim.next()

#get required data from rows
simdata =[[row[2], row[4], eval(row[8])] for row in csvsim]


#add headers

simdata.insert(0, ['Parameter Name', 'Department', 'Is High Good?'])

#print data to seeeee
for item in simdata:
 	print item, ","


#write data to csv file
for item in simdata:
	newfile.writerow(item)


#close files
sim.close()
simdept.close()


#open csv file
ourcsv = open( 'simdept.csv', 'rb')

#set param names
dict = csv.DictReader(ourcsv, fieldnames = ["Parameter Name", "Department", "Is High Good?"])

#print json output
out = json.dumps([row for row in dict])
print(out)

#write to JSON file
csvtojson = open('simdept.json', 'wb')
csvtojson.write(out)

#close files
simdept.close()
csvtojson.close()




