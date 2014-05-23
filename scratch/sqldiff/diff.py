# diff.py 
"""
sqldiff algorithm


inputs: two tables with the same columns, fully sorted
{nb: fully sorted means first sorted on the first column, then by the second to break ties, then by the third.. all the way down to the end; sql's ORDER BY clause performs this for us}

Call the first table L and the second N

start rolling down the tables, searching for identical rows.
Because of the sort, we know that [....] 
 e.g. if the left says [a, 4, q] and the right says [a, 6, g] 
  then you know to advance the left pointer


output: whatever remains in L is the "deletes" list and what is in N is "adds" 


"""

def negativeidx(idx):
    return [-i for i in idx]

def fancyslice(L, idx): #implements indexing-by-set like R and scipy
    return [L[i] for i in idx]

def diff(L, N):
    L, N = iter(L), iter(N)
    Kept_L, Kept_R = [], []
    i_L, i_R = 0, 0
    # start walking the lists
    # this algorithm is not supposed to be, youy know, elegant. i'll get to that.
    L_row = next(L)
    R_row = next(R)
    i = 0
    while True:
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
            if ....:
                print("stepping left")
                i_L += 1
                L_row= next(L)
            else:
                print("stepping right")
                i_R += 1
                R_row= next(R)
            #and the right otherwise..
            
    return fancyslice(L, negativeidx(Erased_L)), fancyslice(R, negativeidx(Kept_R) 

if __name__ == '__main__':
    import sys
    import csv
    L, R = [csv.reader(open(f)) for f in sys.argv[1:]]
    deletions, additions = diff(L, R)
    print(additions)
    print(deletes)
