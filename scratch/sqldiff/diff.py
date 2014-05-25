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

    # a line that is an /update/ is.. marked on the update list and stepped over, I think?
    # because  you've figured out what is up with both rows and dealt with them
    # an
    # but if the rows are totally different
    #  the rows
    # ..my algorithm is going to miss some updates as written?? because how can it possibly detect if
    # like, if I claim that ""
    # instead what I have to do is iterate over all elements and find which ones are the same
    # if ALL are different, that's
    # but how does sorting come into this then?
    # i still need to like, walk
    # sorting ensures that the differences happen at the end
    #  ..h
    # [3]
    # 
    """
    FLAG = None #instructs magic-gen whether to step left, right or eat
    def magicgenerator():
        # yields the current lines to consider
        # carefully handling the cases where either gen might run out
        while True:
    
    def cmp(l, r):
        # compare two rows
        # decide if the two rows are:
        # equal
        # r is an update to l
        # we could do this with the built-in < and == ops, but to check for updatedness we also want to know *where* the elements
        assert len(l) == len(r)
        # TODO: also assert that the types of all elements match up
      
    for left, right in magicgenerator():
       """ 
# this feels sort of like a mergesort, doesn't it?


def coopy(diff):
    "translate a table diff from internal format to [coopy](http://dataprotocols.org/tabular-diff-format/) format"
    raise NotImplemented

def diff(L, R):
    """
    this prototype operates on iterators of lists: the format you get by reading a csv
    XXX bug: it actually is currently hardcoded to require knowing the length of the tables in advance
    
    (perhaps with suitable abstraction into iterables, the same code could run identically whether L and R are SQLAlchemy resultssets, csv.readers, or hard-coded lists)
    
    L is "LOCAL" aka the Left input
    R is "REMOTE" aka the Right input
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
    ops = -1 #DEBUG; count the number of steps the algorithm takes
    try:
        while True:
            ops+=1
            print()
            print(ops)
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
        Kept_L += islice(L, 0, None)
        Kept_R += islice(R, 0, None)

    print(Kept_L)
    print(Kept_R)        
    #return fancyslice(L, Kept_L), fancyslice(R, Kept_R)
    return Kept_L, Kept_R


def diff(L, R):
    "prev impl has bugs; this is one with more preconditions in order to shake them out oin th wash"
    l, r = 0, 0 #left iterator; right iterator
    deletions = []
    additions = []
    while True: #this loop is essentially the merge() part of mergesort(), but with the inner operations changed
                #curious; does that mean it can be factored?
        if l == len(L):
            # patch remaining Rs onto "additions"
            print("break left") #DEBUG
            additions += R[r:]
            break
        
        if r == len(R):
            print("break right") #DEBUG
            # ran out of Rs
            # patch remaining Ls onto "deletions"
            #deletions += L[l:]
            deletions += list(range(l,len(L)))
            break
        
        #print("L[%d] = %s" % (l, L[l]), "R[%d] = %s" % (r, R[r]), "out of %s" % ((len(L),len(R)),))  #DEBUG
        if L[l] == R[r]:
            l += 1
            r += 1
        elif L[l] < R[r]:
            #deletions += [L[l]]
            deletions += [l] #for deletions, we want to know the row ids to delete
            l += 1
        else:
            additions += [R[r]]
            r += 1
        
    return deletions, additions #TODO: swap this API

def diffu(L, R):
    "diff() which returns (additions, updates, deletions)"
    # an "update" as far as we care is a row which shares any of its elements
    # it is typed as this tuple: (id, {columnid: newvalue, ...})
    #  where id is the index of the row in the L table (not in the R table!)
    # a single update takes the place of an addition plus a deletion in diff()
    # we have as a precondition that L and R are sorted from the left column onwards (equivalent to the result of calling sorted() on them)
    # so detecting a change like (a,b,c) -> (a,b,d) is easy
    # detecting (a,b,c) -> (z,b,c) is harder (impossible?)
    #
    raise NotImplemented

def applydiff(Table, additions, deletions):
    """
    preconditions (not enforced): L is a sorted list of rows;
     additions is a sorted list of rows
     deletions is a list of indexes
    """
    assert Table == sorted(Table)
    assert additions == sorted(additions)
    assert all(type(row) is list for row in Table)
    assert all(type(id) is int for id in deletions)
    assert all(0<=id<len(Table) for id in deletions)
    
    # first, remove the deletions
    Table = [l for i, l in enumerate(Table) if i not in deletions]
    
    # add the additions via a mergesort (is mergesort in the stdlib somewhere?)
    # mergesort is: 1) recursively partition the array until you have sorted arrays, ie. single elements (or, if you're more clever, you can use something else when you get to < 10 elts since the recursion overhead outweighs brute force there, usually) 2) as you go up the stack, use merge()
    
    def merge(L, R): #TODO: take *seqs instead of l1, l2 and support an arbitrary number of list TODO: support generic iterables (iter(), StopIteration, etc) 
        # TODO: find this in the stdlib
        l = r = 0
        while l < len(L) or r < len(R):
            #print(l,r,len(L),len(R)) #DEBUG
            if l == len(L):
                # patch remaining Rs
                yield R[r]
                r += 1
                continue
            if r == len(R):
                # patch remaining Rs
                yield L[l]
                l += 1
                continue
            
            if L[l] == R[r]:
                yield L[l]
                yield R[r]
                l += 1
                r += 1
            elif L[l] < R[r]:
                yield L[l]
                l += 1
            else:
                yield R[r]
                r += 1
    
    return list(merge(Table, additions))

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
    
    assert applydiff(L, additions, deletions) == R

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
    assert applydiff(L, additions, deletions) == R

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

# these next two tests are not very interesting if we just have
#  additions/deletions, but are very interesting if there's updates
# will the algorithm detect updates to early columns?

def test_later_column(): 
    L = [[1,2,3,4]]
    R = [[1,2,7,4]]
    
    deletions, additions = diff(L, R)

    print("additions")
    for a in additions:
        print(a)
    print("deletions")
    for d in deletions:
        print(d)
    
    assert applydiff(L, additions, deletions) == R

def test_early_column():
    L = [[1,2,3,4]]
    R = [[7,2,3,4]]
    
    deletions, additions = diff(L, R)

    print("additions")
    for a in additions:
        print(a)
    print("deletions")
    for d in deletions:
        print(d)
    assert applydiff(L, additions, deletions) == R


def test_typical(f1 = "activity_counts.shuf1.csv", f2="activity_counts.shuf2.csv"):
    L, R = [read_table(f) for f in (f1, f2)]
    
    deletions, additions = diff(L, R)

    print("additions")
    for a in additions:
        print(a)
    print("deletions")
    for d in deletions:
        print(d)
    assert applydiff(L, additions, deletions) == R

def tests():
    for name, test in list(globals().items()):
        if not name.startswith("test_"): continue
        
        print("----------------")
        print("TEST:", name)
        test()
        print("----------------")
        print()

test_early_column()

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        test_typical(sys.argv[1], sys.argv[2])
    else:
        tests()
