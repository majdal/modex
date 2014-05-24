#!/usr/bin/env python
# diff.py 
"""
sqldiff algorithm


inputs: two tables with the same columns, fully sorted
{nb: fully sorted means first sorted on the first column, then by the second to break ties, then by the third.. all the way down to the end; sql's ORDER BY clause performs this for us}
(other nb: the particular sort uses doesn't matter, so long as it is consistent from run to run)

Call the first table L and the second N

start rolling down the tables, searching for identical rows.
Because of the sort, we know that [....] 
 e.g. if the left says [a, 4, q] and the right says [a, 6, g] 
  then you know to advance the left pointer


output: whatever remains in L is the "deletes" list and what is in N is "adds" 


"""

from itertools import *

def negativeidx(idx):
    return [-i for i in idx]

def fancyslice(L, idx): #implements indexing-by-set like R and scipy
    # TODO: support negative indexing to mean "drop it"
    return [l for i, l in enumerate(L) if i in idx]

def diff(L, R):
    """
    this prototype operates on iterators of lists: the format you get by reading a csv
    XXX bug: it actually is currently hardcoded to require knowing the length of the tables in advance
    
    (perhaps with suitable abstraction into iterables, the same code could run identically whether L and R are SQLAlchemy resultssets, csv.readers, or hard-coded lists)
    """
    assert L == sorted(L)
    assert R == sorted(R)
    len_L, len_R = len(L), len(R)
    L, R = iter(L), iter(R)
    Kept_L, Kept_R = [], []
    i_L, i_R = 0, 0
    # start walking the lists
    # this algorithm is not supposed to be, youy know, elegant. i'll get to that.
    L_row = next(L)
    R_row = next(R)
    i = -1
    try:
        while True:
            i+=1
            print()
            print(i)
            print("L[%d] = %s" % (i_L, L_row))
            print("R[%d] = %s" % (i_R, R_row))
            # ending conditions are complicated 
            if L_row == R_row:
                # if terms are equal, then erase them both by stepping the index
                print("samesies!")
                L_row = next(L)
                R_row = next(R)
                i_L += 1
                i_R += 1
            else:
                # however if they are different, we need to figure out how different
                print("differences!")
                # we.. step the left if ..
                # TODO: make the common case be 'updated', and 'deleted' be the degenerate update case
                #
                if L_row < R_row:
                    print("stepping left")
                    Kept_L += [(i_L, L_row)]
                    i_L += 1
                    L_row= next(L)
                else:
                    #and the right otherwise..
                    print("stepping right")
                    Kept_R += [(i_R, R_row)]
                    i_R += 1
                    R_row= next(R)
    except StopIteration:
        # finish up any leftovers
        Kept_L += islice(L, i_L, len_L)
        Kept_R += islice(R, i_R, len_R)

    print(Kept_L)
    print(Kept_R)        
    #return fancyslice(L, Kept_L), fancyslice(R, Kept_R)
    return Kept_L, Kept_R

def read_table(fname):
    """
    load a csv , and sort it to serve the preconditions
    drops the header row!
    Inefficient!
    """    
    import csv
    return sorted(list(csv.reader(open(fname,"r")))[1:])

# TODO: rewrite

def test_empty_left():
    L = []
    R = [[-13, 'h', '55'],
         [-9, 'a', '3'],
         [1, 'a', 'q'],]
         
    deletions, additions = diff(L, R)

    print("additions")
    for a in additions:
        print(a)
    print("deletions")
    for d in deletions:
        print(d)


def test_empty_right():
    L = [[-13, 'h', '55'],
         [-9, 'a', '3'],
         [1, 'a', 'q'],]    
    R = []
         
    deletions, additions = diff(L, R)

    print("additions")
    for a in additions:
        print(a)
    print("deletions")
    for d in deletions:
        print(d)

# i need tests...

# one sort of test: construct a list of additions and deletions and updates
# apply them
# then run diff on the results
# and compare the result of diffs

# cases to check for:
#  - a typical case
#  - duplicate rows should be considered distinct!!
#  - what happens if one of the earlier columns is updated; is it detected as an update?
#  - what happens if a mixture of the 
#  - what happens if only one column is updated
#  - having lists of overlap [a, ...], [a, ....]
#  - an empty left (---> ejntirely adds)
#  - an empty right (---> entirely deletes)
#  -

def test_typical(f1 = "activity_counts.shuf1.csv", f2="activity_counts.shuf2.csv"):
    L, R = [read_table(f) for f in (f1, f2)]
    
    deletions, additions = diff(L, R)

    print("additions")
    for a in additions:
        print(a)
    print("deletions")
    for d in deletions:
        print(d)

def tests():
    for name, test in list(globals().items()):
        if not name.startswith("test_"): continue
        print(name)
        test()
        print("----------------")
        print()


if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        test_typical(sys.argv[1], sys.argv[2])
    else:
        tests()
