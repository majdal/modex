#!

# experimenting with MySQL
# this only works with python2 because mysql-python won't build under 3
# (but there are other DB drivers that will talk to MySQL which I haven't tried)

from sqlalchemy import *
import IPython

if __name__ == '__main__':
	# There
	db = create_engine("mysql+mysqldb://root@127.0.0.1:3306/cmombour_sluceiidb") #mysqldb supports specifying a unix socket, but sqlalchemy doesn't seem to expose that. Maybe I just missed it.
	schema = MetaData() #XXX is this a misnomer?
	schema.reflect(db)
	print("These tables available:", schema.tables.keys())

	conn = db.connect() #??? is this necessary? it seems to do things without it..
	
	analysisresults = schema.tables['analysisresults']
	z = select([analysisresults])
	
	IPython.embed()