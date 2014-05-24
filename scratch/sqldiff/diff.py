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
    return sorted(list(csv.reader(open(fname,"r")))[1:])


if __name__ == '__main__':
    import sys
    import csv
    L, R = [read_table(f) for f in sys.argv[1:]]
    deletions, additions = diff(L, R)
    print("additions")
    for a in additions:
        print(a)
    print("deletions")
    for d in deletions:
        print(d)
