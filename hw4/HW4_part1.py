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

def dictPush(d):
    #dictPush pushes the dictionary ‘d’ to the dictstack. 
    #Note that, your interpreter will call dictPush only when Postscript 
    #“begin” operator is called. “begin” should pop the empty dictionary from 
    #the opstack and push it onto the dictstack by calling dictPush.
    return dictstack.append(d)

def define(name, value):
    #add name:value pair to the top dictionary in the dictionary stack. 
    #Keep the '/' in the name constant. 
    #Your psDef function should pop the name and value from operand stack and 
    #call the “define” function.
    leng = len(dictstack)
    if (leng > 0):
        dictstack[leng - 1][name] = value
    else:
        d = {}
        d[name] = value
        dictPush(d)

def lookup(name):
    # return the value associated with name
    # What is your design decision about what to do when there is no definition for “name”? If “name” is not defined, your program should not break, but should give an appropriate error message.
    name = "/" + name
    for d in reversed(dictstack):
        if name in d:
            value = d.get(name)
            return value
    print("name not found")   

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
    for items in reversed(dictstack):
        for k, v in items.items():
            if string == v:
                items[k] = newString

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

def evaluateArray(aInput):
    #should return the evaluated array
    count = len(aInput)
    x = len(opstack)
    for i in aInput:
        # if it is a constant or variable, push it onto the stack
        if ((isinstance(i, int)) or (isinstance(i, bool)) or (isinstance(i, dict)) or (isinstance(i, str) and ((i[0]=='/') or (i[0]=='(')))):
            opPush(i)
        # if it is an operator, perform it, and subtract the number of operator inputs from count
        elif i in operations:
            operations[i]()
            count -= helpCount.get(i)
        else: 
            opPush(lookup(i))
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
    for i in (opstack):
        print(i)

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
def psFor():
    ex = opPop()
    end = opPop()
    step = opPop()
    begin = opPop()
    if begin < end:
        end += 1
    else:
        end -= 1
    #for i in range(begin, end, step):
    while begin != end:
        opPush(begin)
        interpretSPS(ex)
        begin += step

# postscript if operation
def psIf():
    op1 = opPop()
    func = opPop()
    if func == True:
        interpretSPS(op1)

# postscript ifelse operation
def psIfElse():
    op1 = opPop()
    op2 = opPop()
    func = opPop()
    if func == True:
        interpretSPS(op2)
    else:
        interpretSPS(op1)

operations = {"add":add, "sub":sub, "mul":mul, "eq":eq, "lt":lt, "gt":gt, "length":length, 
                  "get":get, "getinterval":getinterval, "putinterval":putinterval, "search":search, 
                  "aload":aload, "astore":astore, "dup":dup, "copy":copy, "count":count, "pop":pop, 
                  "clear":clear, "exch":exch, "stack":stack, "dict":psDict, "begin":begin, 
                  "end":end, "def":psDef, "for":psFor, "if":psIf, "ifelse":psIfElse}

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
            try: # try to convert type to int
                c = int(c)
            except ValueError:
                pass
            if (c == "true") or (c == "false"): # convert true and false to bool
                c = convertBool(c)
            if (type(c) is str) and (c[0] == '[' and c[-1] == ']'): # if token is a string
                c = islist(c)
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
            try: # try to convert type to int
                c = int(c)
            except ValueError:
                pass
            if (c == "true") or (c == "false"): # convert true and false to bool
                c = convertBool(c)
            if (type(c) is str) and (c[0] == '[' and c[-1] == ']'): # if token is a string
                c = islist(c)
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

# COMPLETE THIS FUNCTION 
# This will probably be the largest function of the whole project, 
# but it will have a very regular and obvious structure if you've followed the plan of the assignment.
# Write additional auxiliary functions if you need them. 
def interpretSPS(code): # code is a code array
    for s in code['codearray']:
        if (isinstance(s, int)) or (isinstance(s, bool)):
            opPush(s)
        elif isinstance(s, list):
            opPush(evaluateArray(s))
        elif isinstance(s, dict):
            opPush(s)
        elif isinstance(s,str):
            if (len(s) >= 1) and ((s[0] == '(' and s[-1] == ')')or s[0] == '/'):
                opPush(s)          
            elif s in operations.keys():
                operations[s]()
            else:
                v = lookup(s)
                if v is not None:
                    if isinstance(v, dict):
                        interpretSPS(v)
                    else:
                        opPush(v)
                else:
                    print("interpret error")
        else:
            print("error in PostScript code")

def interpreter(s): # s is a string
    interpretSPS(parse(tokenize(s)))

#clear opstack and dictstack
def clearStacks():
    opstack[:] = []
    dictstack[:] = []

#print(parse(['b', 'c', '{', 'a', '{', 'a', 'b', '}', '{', '{', 'e', '}', 'a', '}', '}']))
#print(parse(['b', 'false', '{', 'a', '{', '1', '2', '}', '{', '{', '(E)', '}', 'true', '}', '}']))

input1 = """
            /square {dup mul} def   
            [3 -2 1]  aload pop
            /total 0 def 
            1 1 3 {pop square total add /total exch def} for 
            total 14 eq stack
         """

input2 = """
            /x 1 def
            /y 2 def
            /x 10 def
            /y 20 def
            0 x 1 y {add} for
            stack
        """
input3 = """
            /f {dup length} def
            [1 2 (322) (451) length]
            [1 -2 4 5 add (long) length]
            (123456)  f
            stack
         """
input4 = """
            /x 1 def
            /y 2 def
            1 dict begin
            /x 10 def
            1 dict begin /y 3 def x y end
            /y 20 def
            x y
            end
            x y
         """
input5 = """
            /sumArray 
            {0 exch aload pop count n sub -1 1 {pop add} for /n n 1 add def } def
            /x 5 def
            /y 10 def
            /n 1 def
            [1 2 3 4 x] sumArray
            [x 7 8 9 y] sumArray
            [y 11 12] sumArray
            [0 0 0] astore
            stack        
         """
input6 = """
            1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq
            stack        
         """
input7 = """
            (CptS322 HW1_CptS355 HW2)
            dup /myclass exch def
            myclass 16 3 getinterval /c exch def
            myclass 4 c putinterval
            myclass
            stack
        """
input8 = """
           (COVID-19 Vaccine)
            dup
            ( ) search pop exch pop
            (-19) search
            {
                pop pop pop (Vaccine) eq
                { (yay) }
                { (???)  }
                ifelse
            } if
            stack
         """

input9 = """
           [1 2 3 4 5] aload /myA exch def
            count copy [0 0 0 0 0] astore
            myA eq
            stack
         """

input10 = """
            /n 5 def
            /fact {
                0 dict begin
                /n exch def
                n 2 lt
                { 1}
                {n 1 sub fact n mul }
                ifelse
                end 
            } def
            n fact
         """

input11 = """
          /fact{
                0 dict
                begin
                    /n exch def
                    1
                    n -1 1 {mul /n n 1 sub def} for 
                end
            } def
            6 fact
         """

input12 = """
        /x 12 def
        /y 8 def
        [x y add 20 eq]
        /n 10 def
        /m 5 def
        [4 n add m lt]
        """

input13 = """
        /y (ani) def
        /x 5 def
        /rosh {
            5 x eq
            {(rosh)}
            {(Not rosh)}
            ifelse
        } def 
        rosh y
        """

input14 = """
        /n = (hello) def
        /m = (world) def
        /y = 10 def
        [14 3 add 7 sub] aload pop
        y eq
        {(world)} if
        n exch
        """

input15 = """
        /y 2 def
        /n 1 def
        /m 3 def
        /final (result) def
        [5 1 3 1] aload pop pop pop pop
        /x exch def 
        /test {
            y n m {x 2 mul} for
        } def final test
        """

input16 = """
        (RoshaniShiwakoti)
        /class (355) def
        /x (is) def
        /y 10 def
        /z (isnt) def
        2 1 3 { 5 2 mul} for y 
        exch pop exch pop exch pop 
        eq
        {x (taking)}
        {z (not taking)} ifelse
        class
        """