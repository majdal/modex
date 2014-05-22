"""
second draft of model logging, using composition instead of inheritence, and dropping the dependency on dataset

the reason using dataset directly is awkward is because it is hard-coded to use its own Table.

the reason this is complicated because we have several cooperating classes kicking around: the database and the tables in that database.

"""


import functools
def funcdebug(f):
    # decorator which traces function calls
    def ff(*args, **kwargs):
        print("DEBUG: %s(%s, %s)" % (f.__name__, args, kwargs))
        return f(*args, **kwargs)
    ff = functools.wraps(f)(ff)
    return ff


#import dataset
#import dataset.persistence.database

import sqlalchemy
from sqlalchemy import *

import uuid #use uuids instead of autoincrementing ids; this requires more storage, but has the advantage that our runs are absolutely uniquely identifiable.


 
#class ModelLog(dataset.Database):
    # ??? how does this fit in    



# TODO: somehow factor the run_id part of TimestepLog into its own classq

# .,. this is a bit weird. There is 1:many sql tables to TimestepTables
# but TimestepTable is setting a default
# ,,this seems.. wrong

# the

class TimestepTable(sqlalchemy.Table):
    def __new__(cls, parent_log, name, *args, **kwargs):
        """
        For some reason I haven't read enough of the code to grok yet,
        the superclass is written in terms of __new__,  instead of __init__
        and it does all sorts of shennigans in there that are hard to work around.
        So, we just pretend that __new__ *is* __init__, as much as possible
        """
        args = ((Column("run_id", Integer, primary_key=True, default=parent_log.run_id), #the default here is a constant and *private*
                Column("time", Integer, primary_key=True, default=lambda: parent_log.time),) +
               args)
        
        self = sqlalchemy.Table.__new__(cls, name, parent_log._metadata, *args, **kwargs) #TODO: use super
        self.parent = parent_log
        
        try:
            self.create() #in contrast to other SQLAlchemy lines, .create() executes itself immediately
        except sqlalchemy.OperationalError as e:
            print("Unable to create table `%s`:" % (name,))
            print(e)
        return self
    
    def __call__(self, **row):
        return self.parent.database.execute(self.insert(row))
            
        
class TimestepLog:
    """
    ...
    
    usage: you need to construct the TimestepTables yourself, in cooperation with this class
     and you must define at least one primary key or you will have trouble
      
     the idea is that you make new TimestepTables to log *new* data
     so the use cases are optimized for that
     
    like so: ...
    tables involved in your database need not necessarily be timestep tables: it is alright to do ._metadata.reflect()
    
    as a convenience, tables are attached as member variables under their name (so your tables need to be named according to python naming rules, which luckily largely overlap with sql naming rules)
    but the proper way to access them is log[name]
     
     TODO: support minimal querying, for completeness
     e.g. a .read() method which does a full select()
     its awkward that the only way to get things out is to grab the internal member .database
    """
    def __init__(self, connection_string):
        self.database = sqlalchemy.create_engine(connection_string)
        self.time = 0
        self.run_id = uuid.uuid4().int & 0xFFFFFFFF #generate a new unique id, then clip it to 32bits because SQL can't handle bigints
        self._metadata = sqlalchemy.MetaData() #create a new metadata for each , so that the column default trick is isolated per-
        self._metadata.bind = self.database
    
    def step(self):
        self.time += 1
    
    def keys(self):
        return self._metadata.tables.keys()
    
    def __getitem__(self, name):
        # rely on the fact that any table adds *itself* to the metadata object
        return self._metadata.tables[name]
    
    def __call__(self, table, **row):
        "syntactic sugar for logging into one of the tables" 
        #TODO: support insert many: if row is a single 
        self[table](**row)
    



if __name__ == '__main__':
    # tests!
    import random
    log = TimestepLog("sqlite://")
    TimestepTable(log, "myawesometable", Column("farmer", sqlalchemy.String, primary_key=True), Column("riches", sqlalchemy.Integer))
    for t in range(20):
        print("Timestep", t)
        for farmer in ["frank", "alysha", "barack"]:
            log('myawesometable', farmer=farmer, riches=random.randint(0, 222))
        #inform the logger that we are going to a new timestep
        log.step()
        
    print(log['myawesometable'].columns.keys())
    for row in log.database.execute(log['myawesometable'].select()):
        print(row)

"""
the sqlalchemy way (let's try to clone that as much as possible)
would be
schema = MetaData()
farmers = Table("farmers", schema, Column("run_id",  primary_key=True), Column("time", primary_key=True), Column("id", INTEGER, primary_key=True), Column("Column("bankaccount", Integer)
farmer_farms = Table("farmer_farms", schema, Column("run_id",  primary_key=True), Column("time", primary_key=True), Column("farm_id"), Column("farmer_id"))

"""
