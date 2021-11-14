
### INTERPRETER FOR OBJECT-ORIENTED LANGUAGE

"""The interpreter processes parse trees of this format:

PTREE ::=  DLIST CLIST
DLIST ::=  []
CLIST ::=  [ CTREE* ]
      where   CTREE*  means zero or more  CTREEs
CTREE ::=  ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST]
        |  ["print", ETREE]
ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE]
      where  OP ::= "+" | "-"
LTREE ::=  ID
NUM   ::=  a nonempty string of digits
ID    ::=  a nonempty string of letters

The interpreter computes the meaning of the parse tree, which is
a sequence of updates to heap storage.

You will extend the above to include declarations and calls of parameterized
procedures.
"""


from heapmodule import *   # import the contents of the  heapmodule.py  module


### INTERPRETER FUNCTIONS, one for each class of parse tree listed above.
#   See the end of program for the driver function,  interpretPTREE


def interpretPTREE(tree) :
    """interprets a complete program tree
       pre: tree is a  PTREE ::= [ DLIST, CLIST ]
       post: heap holds all updates commanded by the  tree
    """
    initializeHeap()
    interpretDLIST(tree[0])
    interpretCLIST(tree[1])
    print("Successful termination.")
    printHeap()


def interpretDLIST(dlist) :
    """pre: dlist  is a list of declarations,  DLIST ::=  [ DTREE+ ]
       post:  memory  holds all the declarations in  dlist
    """
    for dec in dlist :
        interpretDTREE(dec)


def interpretDTREE(d) :
    """pre: d  is a declaration represented as a DTREE:
       DTREE ::=  (WRITE ME)
       post:  heap is updated with  d
    """
    ### WRITE ME
    """
    handle, field = interpretLTREE(d[1])
    if not (handle == activeNS()):
        handle = activeNS()
    """
    handle = activeNS()
    handle, field = interpretLTREE(d[1])
    if not (handle == activeNS()):
        handle = activeNS()
    if d[0] == "int": # ["int", I, ETREE]
        val = interpretETREE(d[2])
        declare(handle,field,val)
    ### HINT METHOD
    elif d[0] == 'proc':
        # closure = {"body": d[4], "params": d[2], "type": d[0], "link":active_ns}

        proc_name = d[1]
        param_list = d[2]
        cmd_list = d[4]
        #handle = allocateNS() # heap[handle] = {} heap = {"h0":{...}, "h1":{}}
        val = allocateClosure(handle,field,[d[0],param_list,d[3],handle])#remove here handle field#just add dic
        #val = interpretETREE(d[2])
        declare(handle,field,val) # heap = {active_ns: {..., proc_name:handle, ...}}
        heap[handle]['type'] = 'proc'
        heap[handle]['params'] = param_list
        heap[handle]['local'] = d[3]
        heap[handle]['body'] = cmd_list
        heap[handle]['link'] = activeNS()
        heap[handle]['parentns'] = handle
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(d[0])
        print(d[1])
        print(d[2])
        print(d[3])
        print(d[4])
        print(activeNS())
        print(handle)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #elif d[0] == "proc": # ["proc",I,ILIST,CLIST]
        #rval = allocateClosure(handle,field,[d[0],param_list,d[3],handle])#remove here handle field#just add dic
        #declare(handle, field, rval) # heap = {active_ns: {..., proc_name:handle, ...}}
    else: crash(d,"invalid declaration")


def interpretCLIST(clist) :
    """pre: clist  is a list of commands,  CLIST ::=  [ CTREE+ ]
                  where  CTREE+  means  one or more CTREEs
       post:  memory  holds all the updates commanded by program  p
    """
    for command in clist :
        interpretCTREE(command)


def interpretCTREE(c) :
    """pre: c  is a command represented as a CTREE:
       CTREE ::=  ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST2]
        |  ["print", LTREE]
       post:  heap  holds the updates commanded by  c
    """
    operator = c[0]
    if operator == "=" :   # , ["=", LTREE, ETREE]
        handle, field = interpretLTREE(c[1])
        rval = interpretETREE(c[2])
        update(handle, field, rval)
    elif operator == "print" :   # ["print", LTREE]
        print(interpretETREE(c[1]))
    elif operator == "if" :   # ["if", ETREE, CLIST1, CLIST2]
        test = interpretETREE(c[1])
        if test != 0 :
            interpretCLIST(c[2])
        else :
            interpretCLIST(c[3])
    # WRITE ME - HINTS
    # interpret ["call", LTREE, ELIST] # ["call", "p", ['1', '2']] if proc p(x, y):...

    elif operator == "call" : # ["call",ID,ELIST]
        handle, field = interpretLTREE(c[1])
        closure = lookupClosure(lookup(handle,field))
        if closure[0] == "proc":
            il = closure[1]
            cl = closure[2]
            newNS = allocateNS()
            update(newNS,"parentns",closure[3])
            el = c[2]
            if len(il) != len(el): # number of parameters don't match
                crash(field, "invalid number of parameters")
            for i,e in zip(il,el):
                declare(newNS,i,interpretETREE(e))
            pushNS(newNS)
            interpretCLIST(cl)
            popNS()

    else :  crash(c, "invalid command")


def interpretETREE(etree) :
    """interpretETREE computes the meaning of an expression operator tree.
         ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE]
         OP ::= "+" | "-"
        post: updates the heap as needed and returns the  etree's value
    """
    if isinstance(etree, str) and etree.isdigit() :  # NUM  -- string of digits
      ans = int(etree)
    elif  etree[0] in ("+", "-") :    # [OP, ETREE, ETREE]
        ans1 = interpretETREE(etree[1])
        ans2 = interpretETREE(etree[2])
        if isinstance(ans1,int) and isinstance(ans2, int) :
            if etree[0] == "+" :
                ans = ans1 + ans2
            elif etree[0] == "-" :
                ans = ans1 - ans2
        else : crash(etree, "addition error --- nonint value used")
    elif  etree[0] == "deref" :    # ["deref", LTREE]
        handle, field = interpretLTREE(etree[1])
        ans = lookup(handle,field)
    else :  crash(etree, "invalid expression form")
    return ans


def interpretLTREE(ltree) :
    """interpretLTREE computes the meaning of a lefthandside operator tree.
          LTREE ::=  ID
       post: returns a pair,  (handle,varname),  the L-value of  ltree
    """
    if isinstance(ltree, str) and  ltree[0].isalpha()  :  #  ID
        ans = (activeNS(), ltree)   # use the handle to the active namespace
    else :
        crash(ltree, "illegal L-value")
    return ans


def crash(tree, message) :
    """pre: tree is a parse tree,  and  message is a string
       post: tree and message are printed and interpreter stopped
    """
    print("Error evaluating tree:", tree)
    print(message)
    print("Crash!")
    printHeap()
    raise Exception   # stops the interpreter
