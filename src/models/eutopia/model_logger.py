"""
model_logger

depends on dataset and therefore SQLAlchemy

usage:

log = ModelLog("sqlite://") # this can be any SQLAlchemy connection string.
log['



"""


import dataset
import uuid #use uuids instead of autoincrementing ids; this requires more storage, but has the advantage that our runs are absolutely uniquely identifiable.


#this code monkey-patches dataset 
#it looks sort of funny because the targets of our monkey patches are considered global variables to dataset
# though they are 
# In any case, patching





dataset.Table = lambda *args, **kwargs: print("hello!!")
q = dataset.connect("sqlite://")
#q['butts'].insert({1:2})
print("is it? ", dataset.connect.__globals__['Table'] is dataset.Table)


    
class ModelTable(dataset.Table):    
    def insert(self, row, *args, **kwargs):
        row = dict(row) #coerce
        row['run_id'] = self.database.id
        return super().insert(row, *args, **kwargs)
    #TODO: finish wrapping the row-related ops, update(), upsert() etc
    

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
        goop = super().get_table.__func__          #this is every bit as sketchy as it looks
                                                   #we're monkeypatching dataset to behave differently
        original = dict(goop.__globals__)
        
        goop.__globals__["Table"] = type(self).__table_class__

        try:
            return super().get_table(*args, **kwargs)
        finally:
            goop.__globals__.update(original)               #put it back



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
        original = dict(dataset.connect.__globals__)
        dataset.connect.__globals__['Database'] = db_class
        try:
            return dataset.connect(*args, **kwargs)
        finally:
            dataset.connect.__globals__.update(original)
    return connect

time_connect = connector(TimestepLog)
model_connect = connector(ModelLog)

if __name__ == '__main__':
    # tests!
    q = time_connect("sqlite://")
    q['myawesometable'].insert({"farmer": "frank", "riches": 10})
    print(q.tables)
    print(list(q['myawesometable'].all()))