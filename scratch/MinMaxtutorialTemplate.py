

#Why do we care about this?
#Python has really nice built-in methods for dealing with CSV files & D2 data 
#is generally in csv form. 

#First, we import the csv library
import csv

# our goal is to have a csv file with only min and max cost for policies 
#written in it ('rb' means we want to read it)
pol = open('Policies.csv','rb')

#with the policies file opened, we run the csv reader method, which 
#parses the file, splitting at commas
csvpol = csv.reader(pol)

#we open a new csv file for costs ('wb'means we'll be writing to it)
costsdept = open('costsdept.csv', 'wb')
#if it doesn't already exist, python creates it

#we now run the csv writer method, which will allow us to write 'rows' into 
#the file as comma separated values
newfile = csv.writer(costsdept)

#but we don't want all the data from pol, we just want the cost data
#we know policy name = row 2, department = 10 mincost= row 11, maxcost = row 12
#let's create an array of data from the policy file

csvpol.next() #we put this here because we don't want headers. they will make
#formatting more difficult (because we can't eval a string!), so we'll
# just skip past them
costdata = [[row[2], row[10], eval(row[11]), eval(row[12])] for row in csvpol]
#we are using the eval function because python by default puts the entries as
#strings, and we want them as integers
#what we've done is created a list where each entry is one 'row' in our csv 
#excel sheet

#now we can add in the headers
#it's helpful to remember that cost data is just a list, so we can use all the
#fun list methods!
costdata.insert(0, ['Policy Name', 'Department', 'mincost', 'maxcost'])


#we can print it to make sure it's what we want (print(costdata))

for item in costdata:
    print item, ","

#we should now be able to write the csv file for min and max cost

for item in costdata:
    newfile.writerow(item)

#so now we have a csv file with just policy names and min and max costs

#make sure to close our files!
pol.close()
costsdept.close()
    


