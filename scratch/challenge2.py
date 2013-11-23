#Once you are able to do this, create another JSON file where the 
#“high-is-good’ value has been modified from 0 or 1 to “good” or “bad”. 
#I think it’s probably easiest to start from csv, but feel free 
#to prove me wrong.

#Import csv and JSON libraries
import csv
import sys
import json

#read from csv file
sim2 = open('simdept.csv', 'rb')


# run csv reader
csvsim2 = csv.reader(sim2)

#open new csv file to write to
sim2rev = open('simdeptrev.csv', 'wb')

#run csv writer
newcsv = csv.writer(sim2rev)

#ignore headers
sim2.next()

#create list for entries
sim2data = [[row[0], row[1], row[2]] for row in csvsim2]
newcsv.writerow(["Parameter Name", "Department", "Is High Good?"])

# print items to verify
for item in sim2data:
 	print item, ","


#replace 0/1 with bad/good
for row in sim2data:

	if row[2] == "0":
		row[2] = "Bad"
	
	else:
		row[2] = "Good"
	newcsv.writerow(row)


#close files
sim2.close()
sim2rev.close()
	

#open modified  file for reading
readcsv = open('simdeptrev.csv', 'rb')

#run dictionary reader
dict = csv.DictReader(readcsv, fieldnames = ["Parameter Name", "Department", "Is High Good?"])

#format dict
out = json.dumps([row for row in dict])

#print output
print(out)

#write to json file
csvtojson = open('simdeptrev.json', 'wb')
csvtojson.write(out)

#close files
readcsv.close()
csvtojson.close()