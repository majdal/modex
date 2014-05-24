sqldiff
=======

An algorithm for computing deltas on tables.

The goal is to be able to turn two snapshots
of a database into a stream of three sorts of events:

* `add({column1: value1, column2: value2, ..., columnN: valueN})` - add a new row 
* `update(rowid, {column2: updated_value2, column3: updated_value3, column5: updated_value5, }...)` - this only sends the updated columns, not the full set
* `delete(rowid)

Instead of updates, we can do a delete and an add at the same time.

Methods Considered
------------------

1. naive: for each line in the first set, find if it's in the second and if not add to deleted list
 for each line in the second set, find if its in the first and if not add to the first 


2.


(2,1) could be implemented in SQL stored procedures, logging results to an "events" table; every time you call the procedure it erases the old table and writes a new one

3. Find a way read the SQL log directly 
  (the equivalent with a journalling filesystem like ext3/ntfs/btrfs would be to parse the log; but not all SQLs necessarily keep such a log

4. construct our own journal
     - use SQL triggers (MySQL, MSSQL, Postgres and Sqlite all have some extension method which you can get to do actions on CREATE, INSERT, UPDATE and DELETEs) and pass the events via IPC/filesystem queue/socket/HTTP
     - rig up a way to export to the filesystem, and then use FAM/inotify/kqueue
         - sqlfuse
         - the sqlite vfs hook
         
5. add timestamp column with automatic updates
  then to get the changes, you do SELECT * from table where ts > last_time_loaded
  ^ but this doesn't handle DELETEs

TODO
----


* [ ] Extend to support delta compression, which is when deltas which cancel each other out in the stream (?? is )
    * ^hmmmmmmmmmm. I *think* that any single run of this algorithm should already cover that case cleanly. delta compression only comes in when you have a series of deltas in a row.
    oh that's interesting then. so we have a time-space tradeoff; or even space in two ways: "physical" space and "delta" space. Delta compression only kicks in if the recipient has lagged out and fallen behind. That is appropriate for dropbox, where the point is syncing with long-term disconnects in between. It's not so important for us, where we want a real-time stream. 

References
-----------

(nothing yet; no readings have been done)
