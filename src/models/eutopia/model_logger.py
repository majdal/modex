"""
model_logger

depends on dataset and therefore SQLAlchemy

usage:

log = ModelLog("sqlite://") # this can be any SQLAlchemy connection string.
log['



"""


import functools

import dataset
import dataset.persistence.database

import uuid #use uuids instead of autoincrementing ids; this requires more storage, but has the advantage that our runs are absolutely uniquely identifiable.


    
class ModelTable(dataset.Table):    
    def insert(self, row, *args, **kwargs):
        row = dict(row) #coerce
        row['run_id'] = self.database.id
        return super().insert(row, *args, **kwargs)
    #TODO: finish wrapping the row-related ops, update(), upsert() etc
    


def funcdebug(f):
    # decorator which traces function calls
    def ff(*args, **kwargs):
        print("DEBUG: %s(%s, %s)" % (f.__name__, args, kwargs))
        return f(*args, **kwargs)
    ff = functools.wraps(f)(ff)
    return ff
 
class ModelLog(dataset.Database):
    __table_class__ = ModelTable
    def __init__(self, *args, **kwargs):
        self.id = self.new_id()
        super().__init__(*args, **kwargs)
    
    @staticmethod
    def new_id():
        #generate a new unique id, then clip it to 32bits because SQL can't handle bigints
        return uuid.uuid4().int & 0xFFFFFFFF 

    def get_table(self, *args, **kwargs):        
        #this code monkey-patches dataset to use our table class instead
        #(but it puts it back immediately!)
        #TODO: is there a way to like, clone the whole loaded package and only tweak some bits?

        original = dataset.persistence.database.Table
        try:
            dataset.persistence.database.Table = type(self).__table_class__
            return super().get_table(*args, **kwargs)
        finally:
            dataset.persistence.database.Table = original



# can metaclass magic D.R.Y. this up?
class TimestepTable(ModelTable):
    def insert(self, row, *args, **kwargs):
        row = dict(row) #coerce
        row['time'] = self.database.time
        return super().insert(row, *args, **kwargs)
    #TODO: finish wrapping the row-related ops, update(), upsert() etc
            
class TimestepLog(ModelLog):
    __table_class__ = TimestepTable
    def __init__(self, *args, **kwargs):
        self.time = 0
        super().__init__(*args, **kwargs)
    def step(self):
        self.time += 1

    

def connector(db_class):
    def connect(*args, **kwargs):
        original,dataset.Database = dataset.Database, db_class
        try:
            return dataset.connect(*args, **kwargs)
        finally:
            dataset.Database = original
    return connect

time_connect = connector(TimestepLog)
model_connect = connector(ModelLog)

if __name__ == '__main__':
    # tests!
    q = time_connect("sqlite://")
    q['myawesometable'].insert({"farmer": "frank", "riches": 10})
    print(q.tables)
    print(list(q['myawesometable'].all()))