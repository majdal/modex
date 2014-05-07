#!

# experimenting with MySQL
# this only works with python2 because mysql-python won't build under 3
# (but there are other DB drivers that will talk to MySQL which I haven't tried)

from sqlalchemy import *

if __name__ == '__main__':
	# There
	db = create_engine("mysql+mysqldb://root@127.0.0.1:3306/cmombour_sluceiidb") #mysqldb supports specifying a unix socket, but sqlalchemy doesn't seem to expose that. Maybe I just missed it.
	schema = MetaData() #XXX is this a misnomer?
	schema.reflect(db)
	print(schema.tables)