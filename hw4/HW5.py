# Roshani Shiwakoti
# consulted with: Taiya Williams (TA)
# WRITE YOUR NAME and YOUR COLLABORATORS HERE

import re

#------------------------- 10% -------------------------------------
# The operand stack: define the operand stack and its operations
opstack = []  #assuming top of the stack is the end of the list

# Now define the HELPER FUNCTIONS to push and pop values on the opstack 
# Remember that there is a Postscript operator called "pop" so we choose 
# different names for these functions.
# Recall that `pass` in Python is a no-op: replace it with your code.

def opPop():
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.
    if not opstack: 
        print("empty stack")
    else: 
        return opstack.pop()

def opPush(value):
    opstack.append(value)

#-------------------------- 16% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []  #assuming top of the stack is the end of the list

# now define functions to push and pop dictionaries on the dictstack, to 
# define name, and to lookup a name

def dictPop():
    # dictPop pops the top dictionary from the dictionary stack.
    return dictstack.pop()

def dictPush(link, d):
    #dictPush pushes the dictionary ‘d’ to the dictstack. 
    #Note that, your interpreter will call dictPush only when Postscript 
    #“begin” operator is called. “begin” should pop the empty dictionary from 
    #the opstack and push it onto the dictstack by calling dictPush.
    tup = (0, d)
    return dictstack.append(tup)

def define(name, value):
    #add name:value pair to the top dictionary in the dictionary stack. 
    #Keep the '/' in the name constant. 
    #Your psDef function should pop the name and value from operand stack and 
    #call the “define” function.
    leng = len(dictstack)
    if (leng > 0):
        dictstack[leng - 1][1][name] = value
    else:
        d = {}
        d[name] = value
        #tup =(0,d)
        dictPush(0, d)

def lookup(name, scope):
    # return the value associated with name
    name = "/" + name
    if not dictstack:
        return "dictstack is empty"
    if scope == "dynamic":
        for tup in reversed(dictstack):
            for v in tup:
                if isinstance(v, dict):
                    if name in v:
                        value = v.get(name)
                        return value
    elif scope == "static": 
        return staticLook(name, len(dictstack)-1)

def staticLook(name, i):
    if name in dictstack[i][1]:
        return dictstack[i][1][name]
    elif i == 0:
        return None
    else:
        found = staticLook(name, dictstack[i][0])
    return found

#--------------------------- 10% -------------------------------------
# Arithmetic and comparison operators: add, sub, mul, eq, lt, gt 
# Make sure to check the operand stack has the correct number of parameters 
# and types of the parameters are correct.
def add():
    v1 = opPop()
    v2 = opPop()
    if (isinstance(v1, int) or isinstance(v1, float)) and (isinstance(v2, int) or isinstance(v2, float)):
        result = v1 + v2
        opPush(result)
    else:
        print("type mismatch")

def sub():
    v1 = opPop()
    v2 = opPop()
    if (isinstance(v1, int) or isinstance(v1, float)) and (isinstance(v2, int) or isinstance(v2, float)):
        result = v2 - v1
        opPush(result)
    else:
        print("type mismatch")

def mul():
    v1 = opPop()
    v2 = opPop()
    if (isinstance(v1, int) or isinstance(v1, float)) and (isinstance(v2, int) or isinstance(v2, float)):
        result = v1 * v2
        opPush(result)
    else:
        print("type mismatch")

def eq():
    v1 = opPop()
    v2 = opPop()
    opPush(v1 == v2)

#less than
def lt():
    v1 = opPop()
    v2 = opPop()
    if (isinstance(v1, int) or isinstance(v1, float)) and (isinstance(v2, int) or isinstance(v2, float)):
        opPush(v2 < v1)
    else:
        print("type mismatch")

#greater than
def gt():
    v1 = opPop()
    v2 = opPop()
    if (isinstance(v1, int) or isinstance(v1, float)) and (isinstance(v2, int) or isinstance(v2, float)):
        opPush(v2 > v1)
    else:
        print("type mismatch")

#--------------------------- 20% -------------------------------------
# String operators: define the string operators length, get, getinterval,  putinterval, search
def length():
    v1 = opPop()
    if isinstance(v1, int) or isinstance(v1, bool):
        opPush(v1)
        pass
    else:
        length=len(v1)
        opPush(length-2)

def get():
    v1 = opPop()
    v2 = opPop() 
    result = (v2[v1+1])
    opPush(ord(result))

def getinterval():
    end = opPop()
    start = opPop()
    string = opPop()
    interval = "("
    for s in string[(start+1):(start+end+1)]:
        interval += s
    interval += ")"
    opPush(interval)

def putinterval():
    replace = opPop()
    index = opPop()
    string = opPop()
    length = len(replace)
    newString = string[0:index+1] + replace[1:-1] + string[index-1+length:]
    for x, i in enumerate(opstack):
        if i == string:
            opstack[x] = newString
    helpPut(string, newString, len(dictstack)-1)

def helpPut(string, newString, i):
    if string in dictstack[i][1]:
        dictstack[i][1][newString]
    elif i == 0:
        return None
    else:
        helpPut(string, newString, dictstack[i][0])

def search():
    seek = opPop()
    string = opPop()
    newString = string[1:-1] # removes the parenthesis
    key = seek[1:-1]
    i = 0
    if string.find(key) == -1:  # string doesn't contain key
        opPush(string)
        opPush(False)
    else:
        for s in newString:  # searches for where they key is
            i += 1   # index of key in string
            if s == key:
                break   # once index is found, stop
        newString = "(" + newString[:(i-1)] + ")"
        string = "(" + string[(i+1):]
        opPush(string)
        opPush(seek)
        opPush(newString)
        opPush(True)

#--------------------------- 18% -------------------------------------
# Array functions and operators:
#      define the helper function evaluateArray
#      define the array operators aload, astore

def evaluateArray(aInput, scope):
    #should return the evaluated array
    count = len(aInput)
    x = len(opstack)
    for i in aInput:
        # if it is a constant or variable, push it onto the stack
        if ((isinstance(i, int)) or (isinstance(i, bool)) or (isinstance(i, dict)) or (isinstance(i, str) and ((i[0]=='/') or (i[0]=='(')))):
            opPush(i)
        # if it is an operator, perform it, and subtract the number of operator inputs from count
        elif i in operations:
            if (i=='if'):
                psIf(scope)
            elif (i=='elseif'):
                psIfElse(scope)
            elif (i=='for'):
                psFor(scope)
            else:
                operations[i]()
            if i in helpCount:
                count -= helpCount.get(i)
        else: 
            opPush(lookup(i, scope))
    l = []
    for i in range(count):
        l.append(0)
    opPush(l)
    astore()
    aInput = opPop()
    return aInput

def aload():
    v1 = opPop()
    if (isinstance(v1, list)):
        for i in (v1):
            opPush(i)
    else:
        print("type mismatch")
    opPush(v1)

def astore():
    emptList = opPop()
    length = len(emptList)
    for i in range(length):
        emptList[length-1] = (opPop()) 
        length -= 1
    emptList = (emptList)  
    opPush(emptList)

#--------------------------- 6% -------------------------------------
# Define the stack manipulation and print operators: dup, copy, count, pop, clear, exch, stack
def dup():
    v1 = opPop()
    opPush(v1)
    opPush(v1)

def copy():
    numCopy = opPop()
    for i in opstack[-numCopy:]:
        opPush(i)

def count():
    opPush(len(opstack))
    return len(opstack)

def pop():
    return opPop()

def clear():
    opstack.clear()
    dictstack.clear()

def exch():
    v1 = opPop()
    v2 = opPop()
    opPush(v1)
    opPush(v2)

def stack():
    print("==============”")
    for i in reversed(opstack):
        print(i)
    print("==============”")
    for i in reversed(dictstack):
        print(i)
    print("==============”")

#--------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python. Similarly, call the function for dict operator as psDict.
# Note: The psDef operator will pop the value and name from the opstack and call your own "define" operator (pass those values as parameters).
# Note that psDef()won't have any parameters.
def psDict():
    v1 = opPop()
    d = {}
    opPush(d)

def begin():
    d = opPop()
    dictPush(d)

def end():
    dictPop()

def psDef():
    value = opPop()
    key = opPop()
    if isinstance(key, str):
        define(key, value)
    else:
        print("Type mismatch")

#------------------------------ Part Two -------------------------------

# COMPLETE THIS FUNCTION
# The it argument is an iterator.
# The tokens between '{' and '}' is included as a sub code-array (dictionary). If the
# parenteses in the input iterator is not properly nested, returns False.

# for loop function 
def psFor(scope):
    ex = opPop()
    end = opPop()
    step = opPop()
    begin = opPop()
    if begin < end:
        end += 1
    else:
        end -= 1
    for i in range(begin, end, step):
        opPush(begin)
        interpretSPS(ex, scope)
        begin += step

# postscript if operation
def psIf(scope):
    op1 = opPop()
    func = opPop()
    if func == True:
        interpretSPS(op1, scope)

# postscript ifelse operation
def psIfElse(scope):
    op1 = opPop()
    op2 = opPop()
    func = opPop()
    if func == True:
        interpretSPS(op2, scope)
    else:
        interpretSPS(op1, scope)

# stores operations and their function calls
operations = {"add":add, "sub":sub, "mul":mul, "eq":eq, "lt":lt, "gt":gt, "length":length, 
                  "get":get, "getinterval":getinterval, "putinterval":putinterval, "search":search, 
                  "aload":aload, "astore":astore, "dup":dup, "copy":copy, "count":count, "pop":pop, 
                  "clear":clear, "exch":exch, "stack":stack, "dict":psDict, "begin":begin, 
                  "end":end, "def":psDef}

# stores the number of pops it takes to reduce list size for every relevant operation-- helper for evaluate array
helpCount = {"add":2, "sub":2, "mul":2, "eq":2, "lt":2, "gt":2, "length":1, "begin":2,
                  "get":2, "getinterval":3, "putinterval":3, "search":1, "exch":1, "copy":1,
                  "aload":1, "astore":1, "dict":2, "begin":1, "end":1, "def":3, "for":4}

def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[\[][a-zA-Z-?0-9_\s\(\)!][a-zA-Z-?0-9_\s\(\)!]*[\]]|[\()][a-zA-Z-?0-9_\s!][a-zA-Z-?0-9_\s!]*[\)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)  

def groupMatch(it):
    res = []
    for c in it:
        if c == '}':
            return {'codearray':res}
        elif c=='{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code-array for the inner 
            # parenthesis, it will be appended to the list we are constructing 
            # as a whole.
            res.append(groupMatch(it))
        else:
            # typecasts ints bools and converts lists
            c = helpcast(c)
            res.append(c)
    return False

# COMPLETE THIS FUNCTION
# Function to parse a list of tokens and arrange the tokens between { and } braces 
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested dictionaries.
def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c=='}':  #non matching closing parenthesis; return false since there is 
                    # a syntax error in the Postscript code.
            return False
        elif c=='{':            # checks if it is another codearray, if it is, recurse
            res.append(groupMatch(it))
        else:
            # check value type 
            c = helpcast(c)
            res.append(c)
    return {'codearray':res}

# converts a true and false string to their correct boolean values
def convertBool(c):
    return c == "true"

# if the token is a list, convert it to a python list ex: '[1 2 3 4]' = [1,2,3,4]
def islist(s):
    # ex s = '[3, 2, 1]''
    newList = []
    # splits the spaces, gets rid of the brackets and updates string value
    s = s[1:-1].split(' ')
    for c in s:
        try: 
            c = int(c)        # convert string to int
        except ValueError:
            pass
        if type(c) is list:
            newList.append(islist(c))    # if it is a list, recurse
        else:
            newList.append(c)    # append the value
    return newList

# helper method which casts bools, ints and chekcs if token is a list -- in order to reduce redundancy
def helpcast(c):
    try: # try to convert type to int
        c = int(c)
    except ValueError:
        pass
    if (c == "true") or (c == "false"): # convert true and false to bool
        c = convertBool(c)
    if (type(c) is str) and (c[0] == '[' and c[-1] == ']'): # if token is a list
        c = islist(c)
    return c

# COMPLETE THIS FUNCTION 
# This will probably be the largest function of the whole project, 
# but it will have a very regular and obvious structure if you've followed the plan of the assignment.
# Write additional auxiliary functions if you need them. 
def interpretSPS(code, scope): # code is a code array, scope is static or dynamic
    for s in code['codearray']:
        if (isinstance(s, int)) or (isinstance(s, bool)):
            opPush(s)
        elif isinstance(s, list):
            opPush(evaluateArray(s, scope))
        elif isinstance(s, dict):
            opPush(s)
        elif isinstance(s,str):
            if (len(s) >= 1) and ((s[0] == '(' and s[-1] == ')')or s[0] == '/'):
                opPush(s)          
            elif s in operations.keys():
                operations[s]()
            elif (s=='if'):
                psIf(scope)
            elif (s=='ifelse'):
                psIfElse(scope)
            elif (s=='for'):
                psFor(scope)
            else:
                v = lookup(s, scope)
                if v is not None:
                    if isinstance(v, dict):
                        dictPush(staticLink(s), {}) # replace 0 with staticlink later
                        interpretSPS(v, scope)
                        dictPop()
                    else:
                        opPush(v)
                else:
                    print("interpret error")
        else:
            print("error in PostScript code")

#parses the input string and calls the recursive interpreter to solve the
#program
def interpreter(s, scope):
    tokenL = parse(tokenize(s))
    interpretSPS(tokenL,scope)

#clear opstack and dictstack
def clearBoth():
    opstack[:] = []
    dictstack[:] = []

# ------ SSPS functions -----------
# search the dictstack for the dictionary "name" is defined in and return the (list) index for that dictionary (start searhing at the top of the stack)
def staticLink(name):
    # create a staticlinkhelper(token) which returns staticlink index
    return staticHelp(name, len(dictstack)-1)

def staticHelp(name, i):
    if name in dictstack[i][1]:
        return i
        # return i? we want to return the index
    elif i == 0:
        return None
    else:
        return staticHelp(name, dictstack[i][0])

# staticlink method OK

########################################################################
####  ASSIGNMENT 5 - SSPS TESTS
########################################################################

def sspsTests():

    testinput1 = """
    /x 4 def
    /g { x stack } def
    /f { /x 7 def g } def
    f
    """

    testinput2 = """
    /x 4 def
    (static_?) dup 7 (x) putinterval /x exch def
    /g { x stack } def
    /f { /x (dynamic_x) def g } def
    f
    """

    testinput3 = """
    /m 50 def
    /n 100 def
    /egg1 {/m 25 def n} def
    /chic
    	{ /n 1 def
	      /egg2 { n stack} def
	      m  n
	      egg1
	      egg2
	    } def
    n
    chic
        """

    testinput4 = """
    /x 10 def
    /A { x } def
    /C { /x 40 def A stack } def
    /B { /x 30 def /A { x } def C } def
    B
    """

    testinput5 = """
    /x 2 def
    /n 5  def
    /A { 1  n -1 1 {pop x mul} for} def
    /C { /n 3 def /x 40 def A stack } def
    /B { /x 30 def /A { x } def C } def
    B
    """

    testinput6 = """
    /out true def 
    /xand { true eq {pop false} {true eq { false } { true } ifelse} ifelse dup /x exch def stack} def 
    /myput { out dup /x exch def xand } def 
    /f { /out false def myput } def 
    false f
    """

    testinput7 = """
    /x [1 2 3 4] def
    /A { x aload pop add add add } def
    /C { /x [10 20 30 40 50] def A stack } def
    /B { /x [6 7 8 9] def /A { x } def C } def
    B
    """

    testinput8 = """
    /x [2 3 4 5] def
    /a 10 def  
    /A { x } def
    /C { /x [a 2 mul a 3 mul dup a 4 mul] def A  a x stack } def
    /B { /x [6 7 8 9] def /A { x } def /a 5 def C } def
    B
    """

    testinput9 = """
    /y 10 def
    /x 11 def
    /A { y } def 
    /B { /x [1 2 3] def A stack} def
    /C { /y x 2 mul 3 add def B} def
    C
    """

    testinput10 = """
    /x 2 def
    /n 12 def
    /A { /x 10 def } def
    /C { /n 4 def 1 1 eq { 2 2 add} { 3 3 sub} ifelse A stack} def
    /B { /x 20 def /A { n } def C } def
    B
    """

    testinput11 = """
    /x 4 def 
    /n 10 def
    /R { /n 20 def } def
    /y { /n 5 def x 11 eq {2 10 add} {5 6 mul} ifelse R stack} def 
    /A { /x 10 def /R { n } def y} def 
    A
    """

#interpreter(testinput8, "static")

    ssps_testinputs = [testinput1, testinput2, testinput3, testinput4, testinput5, testinput6, testinput7, testinput8, testinput9, testinput10, testinput11]
    i = 1
    for input in ssps_testinputs:
        print('TEST CASE -',i)
        i += 1
        print("Static")
        interpreter(input, "static")
        clearBoth()
        print("Dynamic")
        interpreter(input, "dynamic")
        clearBoth()
        print('\n-----------------------------')

sspsTests()
