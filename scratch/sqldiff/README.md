sqldiff
=======

An algorithm for computing deltas on tables.


Methods Considered
------------------

1.


2.


3.

4.

5.

TODO
----


* [ ] Extend to support delta compression, which is when deltas which cancel each other out in the stream (?? is )
    * ^hmmmmmmmmmm. I *think* that any single run of this algorithm should already cover that case cleanly. delta compression only comes in when you have a series of deltas in a row.
    oh that's interesting then. so we have a time-space tradeoff; or even space in two ways: "physical" space and "delta" space. Delta compression only kicks in if the recipient has lagged out and fallen behind. That is appropriate for dropbox, where the point is syncing with long-term disconnects in between. It's not so important for us, where we want a real-time stream. 

References
-----------

(nothing yet; no readings have been done)
