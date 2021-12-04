
### INTERPRETER FOR OBJECT-ORIENTED LANGUAGE

"""The interpreter processes parse trees of this format:

PTREE ::=  [DLIST, CLIST]
DLIST ::=  [ DTREE* ]
           where  DTREE*  means zero or more DTREEs
DTREE ::=  ["int", ID, ETREE]  |  ["proc", ID, IDLIST, DLIST, CLIST]
            |  ["ob", ID, ETREE] |  ["class", ID, TTREE] 

CLIST ::=  [ CTREE* ]
CTREE ::=  ["=", LTREE, ETREE]  |  ["if", ETREE, CLIST, CLIST]
        |  ["print", ETREE]  |  ["call", LTREE, ELIST]

ELIST ::=   [ ETREE* ]
ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE]  |  "nil"  |  ["new",  TTREE]
      where  OP ::=  "+"  | "-"
TTREE ::=  ["struct", DLIST] |  ["call", LTREE] 
LTREE ::=  ID  | ["dot", LTREE, ID]

NUM   ::=  a nonempty string of digits
IDLIST ::= [ ID* ]
ID    ::=  a nonempty string of letters

This is extended from the parse tree in project 2 to include object declarations and class.

========================
In Part C, the new to project 2 language syntax are:

D ::=  ...  |  ob I = E  
E ::= ... |  new T  |  nil
T ::=  { DL }
L ::=  I  |  L . I

Corresponding addition to parser tree are:

DTREE ::=   ... |  ["ob", ID, ETREE]
ETREE ::=  ...  |  "nil"  |  ["new",  TTREE]
TTREE ::=  ["struct", DLIST]
LTREE ::=  ID  |  ["dot", LTREE, ID]

========================

In Part D, we have two addition to the syntax: 

D ::=  ...  |  class I : T
T ::=  ...  |  L

Correspoinding addition to parser tree format are:

DTREE ::=  ...  |  ["class", ID, TTREE]
TTREE ::=  ...  |  ["call", LTREE]

=======================

This files only show the part you will need to implement for Part C and D, 
you should add these new implementation to your Project 2 to finish the whole project.

"""

def interpretETREE(etree) :
    """interpretETREE computes the meaning of an expression operator tree.
         ETREE ::=  NUM  |  [OP, ETREE, ETREE] |  ["deref", LTREE]  |  "nil"  |  ["new",  TTREE]
      where  OP ::=  "+"  | "-"
        post: updates the heap as needed and returns the  etree's value

    Within interpretETREE, 
    1. implement "nil" to have itself as its value. 
    2. Implement ["new", T] to call interpretTTREE(T), 
    whose job is to allocate an object, fill it with T, and return the object's handle.
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

    # Part C: WRITE ME 
    # 1. implement "nil" to have itself as its value.
    elif isinstance(etree,str) and (etree == "nil") :   # "nil"
        ans = "# WRITE ME"
    
    # 2. Implement ["new", T] to call interpretTTREE(T), 
    #whose job is to allocate an object, fill it with T, 
    #and return the object's handle.
    elif etree[0] == "new" :   # ["new", TTREE]
       ans = " # WRITE ME"
       
    else :  crash(etree, "invalid expression form")
    return ans

# Part C and D: WRITE ME 
def interpretTTREE(ttree) :
    """ interpret a struct declaration.
        pre: TTREE ::=  ["struct", DLIST] |  ["call", LTREE] 
        post: returns the handle to the struct and updates heap as needed

        Part C: add interpretation for : TTREE ::=  ["struct", DLIST] 

        You define def interpretTTREE(ttree). 
        It receives arguments of the form, ["struct", DLIST]. 
        The function does this: 
        (i) allocates a new namespace and pushes the namespace's handle on 
        the activation stack; 
        (ii) evaluates DLIST; 
        (iii)pops the activation stack and returns the popped handle as its answer.

        Part D: add interpretation for TTREE ::=  ["call", LTREE] 

        Within interpretTTREE, implement ["call", LTREE]. 
        This works like procedure call, where LTREE is computed to a handle,
         the closure labelled by the handle is extracted from the heap, 
         and provided that the closure holds a class,
         the TTREE within the closure is extracted and executed.


    """
    global activeStack
    ans = "" # returned variable

    # Part C: WRITE ME
    if ttree[0] == "struct" :   # ["struct", DLIST]
        currentNS = activeNS()
        #(i) allocates a new namespace 
        # and pushes the namespace's handle on the activation stack; 
         
        # WRITE ME

        #(ii) evaluates DLIST; 
        # WRITE ME

        # (iii)pops the activation stack and returns the popped handle as its answer.
        # WRITE ME
        
        ans = "# WRITE ME"
    
    # Part D: WRITE ME 
    elif ttree[0] == "call" :    # ["call", LTREE]
        '''This works like procedure call, where 
         the closure labelled by the handle is extracted from the heap, 
         and provided that the closure holds a class,
         the TTREE within the closure is extracted and executed.
         '''
        # (i) LTREE is computed to a class handle, 
        # the closure labelled by the handle is extracted from the heap

        ns, className = "# WRITE ME" 
        classHandle = "# WRITE ME"

        #provided that the closure holds a class,
        if lookup(classHandle,"type") ==  "class":
            # then the TTREE within the closure is extracted and executed.
            body = "# WRITE ME " 

            pushHandle(ns)
            ans = "# WRITE ME "
            popHandle()
            update(ans, "parentns", activeNS())

        else :
            crash(ttree, "invalid classname, cannot create object")
    
    else :
        crash(ttree, "ttree is not a struct paser tree")
    return ans




def interpretDTREE(d) :
    """pre: d  is a declaration represented as a DTREE:
            DTREE ::=  ["int", ID, ETREE]  |  ["proc", ID, IDLIST, DLIST, CLIST]
                        |  ["ob", ID, ETREE] |  ["class", ID, TTREE]
                 # Note:  DLIST in ["proc", ID, IDLIST, DLIST, CLIST]
                  holds the local decs if you have done Part B; 
                 it is empty (no local declarations) if you only implement Part A.
       post:  heap is updated with  d
    """
    currentNS = activeNS()
    if d[0] == "int" :   # ["int", ID, ETREE]
        pass # refer to your Part A

    elif d[0] == "proc" :   # ["proc", ID, ILIST, DLIST, CLIST]
        pass # refer to your Part A

    # Part C
    # 1. WRITE ME for object declaration
    # syntax: ob I = new T or ob I = "nil"
    # parser tree ["ob", ID, ETREE]
    elif d[0] == "ob" :  
        # (i) computes the meaning of ETREE,  
        obHandle = "# WRITE ME"
       
        # (ii) validates that ETREE is either a handle to an object or is nil,
        if "# WRITE ME" : 
            #(iii) binds ID to the meaning in the active namespace 
            # (provided that ID is not already declared there).

            declare("# WRITE ME")

        else :
            crash (d, "not an object handle")
    
    
    # Part D: WRITE ME
    # implement ["class", ID, TTREE], 
    # which behaves like procedure declaration, 
    # that is, ID is bound to a closure containing TTREE 
    # and its link to global variables. 

    elif d[0] == "class" :   # ["class", ID, TTREE]
        # WRITE ME 

        
    else :
        crash(d, "invalid declaration")




def interpretLTREE(ltree) :
    """interpretLTREE computes the meaning of a lefthandside operator tree.
          LTREE ::=  ID | ["dot", LTREE, ID]
       post: returns a pair,  (handle,varname),  the L-value of  ltree

    Part C: implement ["dot", LTREE, ID]. 
    This means you compute the handle named by LTREE, 
    call it h, and then check if the pair, (h,ID) is a valid L-value 
    (that is, variable ID is a field inside the object named by h).
    """
    
    if isinstance(ltree, str) and  ltree[0].isalpha()  :  #  ID
        pass # refer to your Project implementation


    # Part C: WRITE ME               
    # implement ["dot", LTREE, ID]
    elif isinstance(ltree, list) and ltree[0] == "dot" :   #["dot", LTREE, ID]
        
        # compute the handle named by LTREE
        han,name = "# WRITE ME"   
        h = "# WRITE ME"
        
        # check if the pair, (h, ID) is a valid L-value 
        if "# WRITE ME" :
            ans = "# WRITE ME"  # compute the vlaue of
        else :
            crash(ltree, "field not defined in the object")
    else :
        crash(ltree, "illegal L-value")
    if ans :
        return ans
    else :
        crash(ltree, " can not interpret either because it's not defined or it's not stored in heap")


def crash(tree, message) :
    """pre: tree is a parse tree,  and  message is a string
       post: tree and message are printed and interpreter stopped
    """
    print "Error evaluating tree:", tree
    print message
    print "Crash!"
    printHeap()
    raise Exception   # stops the interpreter




