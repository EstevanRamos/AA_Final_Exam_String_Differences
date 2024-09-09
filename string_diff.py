# UTEP CS5350 Advanced Algorithms - Code for Final Exam
#
# String Editing Functions
#
# First Name of Student: Estevan
# Last Name of Student:  Ramos
#
# Students must not add any other functions to this file and must not
# add any import statements to use code defined outside this file.
#
#

import sys

def memoize(f):
    """Memoization function

       To be used with a memoization decorator.

       Students must not modify this function.

    """
    memo = {}
    def helper(*n):
        if n not in memo:
            memo[n] = f(*n)
        return memo[n]
    return helper


def apply_edit_list(s, l):
    """Applies an edit list l on a string s

       The string s is a string of any length.

       The list l contains tuples, each with 3 elements:

        * The first element a in the tuple is a string.
        * The second element p in the tuple is an integer.
        * The third element d in the tuple is either an integer or a
          string.

       The string a stands for the action. It is either 'd' for
       'delete' or 'i' for 'insert'.

       The integer p stands for a position in the string, starting
       with 0 for the first character of the string.

       The third element d stands for data.

       If the action a is 'd' ('delete'), then the data d must be an
       integer. It indicates how many characters get deleted, starting
       from (and including) the character at position p.

       If the action a is 'i' ('insert'), then the data d must be a
       string. It stands for the string to be inserted, before the
       character at position p.

       For example,

       apply_edit_list("Hello", [('d', 1, 3), ('i', 2, 'la')])

       yields "Hola".

       All positions and lengths must be well-defined, i.e.  the must
       be inside the current string. All actions, positions and
       lengths that are not well defined are silently ignored.

       Students must not modify this function.

    """
    t = s
    for e in l:
        lt = len(t)
        (a, p, d) = e
        if a == 'd':
            if isinstance(d, int) and (0 <= p) and (0 <= d) and (p+d <= lt):
                t = t[:p] + t[p+d:]
        elif a == 'i':
            if isinstance(d, str) and (0 <= p) and (p <= lt):
                t = t[:p] + d + t[p:]
    return t


@memoize
def try_compact_edit_steps(u, v):
    """Checks if the edit steps u and v, to be executed in this order, can
       be fused into a single edit step.

       If no fusion is possible, returns None.

       Otherwise, returns a fused edit step.

       Students must not modify this function.

    """
    ua, up, ud = u
    va, vp, vd = v

    if ua != va:
        return None

    if ua == 'i':
        if isinstance(ud, str) and isinstance(vd, str):
            if up == vp:
                return ('i', up, vd + ud)
            if vp == up + len(ud) - 1:
                return ('i', up, ud + vd)
            return None
        else:
            return None

    if ua == 'd':
        if isinstance(ud, int) and isinstance(vd, int):
            if up == vp:
                return ('d', up, ud + vd)
            if up == vp + vd:
                return ('d', vp, ud + vd)
            return None
        else:
            return None

    return None


def compact_edit_list(l):
    """Compacts an edit list l by fusing repeated deletions and
       insertions that can be fused into a single deletion of more
       characters or into a single insertion of a longer string.

       Proceeds recursively.

       Students must not modify this function.

    """
    if len(l) == 0:
        return l

    h = l[-1]
    t = l[:-1]
    u = compact_edit_list(t)

    if len(u) == 0:
        return [ h ]

    es = try_compact_edit_steps(u[-1], h)
    if es is not None:
        return compact_edit_list(u[:-1] + [ es ])
    else:
        return u + [ h ]


def edit_list_num_deletions(l):
    """Returns the sum of the number of characters deleted by valid 'd'
       ('delete') actions in the edit list l.

       Does not call any other function besides the isinstance
       operator, comparison of strings and the addition operator.

       Students must not modify this function.

    """
    c = 0
    for e in l:
        a, p, d = e
        if a == 'd':
            if isinstance(d, int):
                c = c + d
    return c


def edit_list_cheaper(la, lb):
    """Returns True iff the edit cost of la is cheaper than the 
       one for lb.

       An edit list la has a cheaper edit cost if la performs
       less deletions or performs the same number of deletions
       but is shorter.

       Calls edit_list_num_deletions, uses len. Does not use any other
       function besides integer comparisons.

       Students must not modify this function.

    """
    lad = edit_list_num_deletions(la)
    lbd = edit_list_num_deletions(lb)
    if lad < lbd:
        return True
    if lad > lbd:
        return False
    return len(la) < len(lb)
    

@memoize
def generate_edit_list(s, t, offset = 0):
    """Generates an edit list to be given to apply_edit_list. The edit
       list is formed such that the string s gets transformed into the
       string t.

       Among all possible edit lists transforming s into t returns the
       one that reutilizes best the longest common sub-sequence of
       characters in the two strings s and t. In the case two (or
       more) edit lists reutilizing best the longest common
       sub-sequence of characters in the two strings s and t exist,
       returns the one that is shortest.
    
       This optimization property is captured by the edit_list_cheaper
       function defined above, which this function must call.

       It is important to note that any string s can be edited into a
       string t with a edit list of length 2: the string s is first
       deleted entirely, then the string t is inserted into the empty
       string. However, although this edit list of length 2 may be
       short (and even the shortest edit list possible), it does not
       reutilize at all the longest common sub-sequence of characters
       in the two strings s and t.

       The function uses the helper function compact_edit_list to
       compact sublists of edit lists that perform repeated deletions
       or repeated insertions. However, compact_edit_list must not
       called if it can be shown statically (when writing the code)
       that the possible call to compact_edit_list would not result in
       a shorter edit list.

       It is important to ensure that the use of compact_edit_list
       does not infringe on the guarantee that generate_edit_list
       gives, namely that the longest common sub-sequence of
       characters in the strings s and t gets used the best.
       
       The generate_edit_list function uses dynamic programming
       through memoization.

       The function checks for the following cases in particular:

        * s and t are equal
        * s is empty, t is not
        * s is not empty, t is empty
        * s and t start with the same character
             + s and t also end with the same character
             + s and t end with a different character
        * s and t end with the same character, but do not start with
          the same character

       In the case when s and t start with different characters and
       end with different characters, it is possible to anchor the new
       edit sequence search at the first character of s, at the first
       character of t, at the last character of s or the last
       character of t. In any case, the shortest edit list best
       reutilizing the longest common sub-sequence of characters gets
       returned.

       Care needs to be used when working on edit lists: the positions
       in edit lists are relative to the string currently found in the
       temporary buffer (variable t in function apply_edit_list). An
       edit list valid to transform a substring of s into a substring
       of t is not necessarily a valid edit list on the whole string
       s.

       Besides calling itself recursively, calling compact_edit_list,
       calling edit_list_cheaper and using the string and list
       modification functionalities of Python as well as the len
       operator, the function generate_edit_list must not call any
       other function.

       Students must design and implement this function.

    """
    if s == t:
        return []
    
    if not s and not t:
        return []
    
    if not s and t:
        return [('i' , offset , t)]
    
    if s and not t:
        return[('d', offset, len(s))]
    
    if s[0] == t[0]:
        if s[-1] == t[-1]: 
            #check going from the begging
            beggining = generate_edit_list(s[1:], t[1:] , offset+1)
            #check going from the ending 
            ending = generate_edit_list(s[:-1], t[:-1], offset)

            if edit_list_cheaper(beggining, ending):
                return beggining
            else:
                return ending
        else:
            return generate_edit_list(s[1:], t[1:] , offset+1)
    elif s[-1] == t[-1]:
        return generate_edit_list(s[:-1],t[:-1],offset)
    else:
        #anchor at first char of s
        insert = compact_edit_list([('i', offset, t[0])] +generate_edit_list(s, t[1:], offset+1))
        #annchor of first char of t
        delete = compact_edit_list([('d', offset, 1)] + generate_edit_list(s[1:],t,offset))
        
    
    if edit_list_cheaper(insert, delete):
        return insert
    else:
        return delete
    
    #examples run
    # "hello" "howdy"-> The edit list to convert "hello" to "howdy" is [('d', 1, 3), ('i', 2, 'wdy')]
    # "hello" "goodbye" -> The edit list to convert "hello" to "goodbye" is [('d', 0, 4), ('i', 0, 'g'), ('i', 2, 'odbye')]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough arguments. Give two strings as two arguments.")
        sys.exit(1)

    err_code = 0
    try:
        s = sys.argv[1]
        t = sys.argv[2]
        u = generate_edit_list(s, t)
        r = apply_edit_list(s, u)
        if t == r:
            print("The edit list to convert \"{}\" to \"{}\" is {}".format(s, t, u))
        else:
            print("Could not find a correct edit list for s = \"{}\" and t = \"{}\".".format(s, t))
            print("The edit list u = {}".format(u))
            print("applied onto s = \"{}\" yields the incorrect string r = \"{}\".".format(s, r))
            err_code = 1
    except:
        print("An exception occurred computing an edit list for \"{}\" and \"{}\".".format(sys.argv[1], sys.argv[2]))
        err_code = 1

    sys.exit(err_code)