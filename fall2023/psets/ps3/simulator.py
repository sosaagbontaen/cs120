# Simulator file for question 1.
# Fill in the implementation of the different commands of the simulator.
# You can use `tests.py` to run your simulator on some prewritten RAM programs.

from collections import defaultdict

def printState(var_list, mem_dict, input_arr, program_arr):
    print("=============== P R O G R A M =========================================== ")
    print("Commands :", program_arr)
    print("=============== I N P U T =========================================== ")
    print(input_arr)
    print("=============== V A R I A B L E S =================================== ")
    print("Variables :",var_list,"\nInput Length:",var_list[0],
          "\nOutput Pointer:",var_list[1],
          "\nOutput Length:",var_list[2])
    print("===============  M E M O R Y ========================================")
    for key, value in mem_dict.items():
        print("(",key,",", value,") |")
    print("=====================================================================")

variableList = []
# Note: defaultdict works exactly the same as a normal Python dictionary except it returns a default 
#       value (in this case, 0) when accessing a key that is not defined rather than raising KeyError.
#       We are using a dictionary rather than a list/array to manage the memory so that we don't need to 
#       initialize and store memory cells that are never accessed by the RAM program.
memory = defaultdict(int)

# Creates the variable list and the memory dictionary.
# Initializes the 0th variable, input_len, to be the first element of the program array.
def setupEnv(programArr, inputArr):
    variableList.clear()
    memory.clear()

    ## @deletelater
    # It's just initializing the variableList based on the # of variables specified by v (AKA programArr[0])
    # Remember, programArr looks like [v, C0, C1, ... C_l-1], where v is just a number
    for i in range(programArr[0]):
        variableList.append(0)
    
    ## @deletelater
    # initialize 0th variable to be input length
    variableList[0] = len(inputArr)
    ## @delete later
    # stores the input in the memory dictionary
    for i in range(len(inputArr)):
        memory[i] = inputArr[i]
        
# Runs the given RAM program on the input.
def executeProgram(programArr, inputArr):
    setupEnv(programArr, inputArr)
    
    ##@deletelater
    # Disregards the variablecounter. We don't need it anymore b/c we've already
    # initialized our variableList
    programArr = programArr[1:]

    ##@deletelater
    #keeps track of the line we're on?
    programCounter = 0

    while programCounter < len(programArr):
        # Store the command and the list of operands.
        ##@deletelater | cmd saves the actual name of the command that we're currently on (determined by programcounter)
        # and ops (operands) saves the indices of the variables or line numbers used in the command that we're currently on
        # remember, C_i = [cmd_name, i, j, k] (j and k are not necessary)
        cmd = programArr[programCounter][0]
        ops = programArr[programCounter][1:]
        
        # Assignment commands
        if cmd == "read":       
            # ['read', i, j]: lookup the var_j location in memory and assign that value to var_i
            ## @deletelater : here, ops[0] = i, ops[1] = j, variableList[j], variableList[ops[0]] = variableList[var_i] = var_i
            #remember, for this pset, we're assuming the variables are named 0,...v-1. so the 3rd variable is named 3
            # this means that if ops[1] = j then variableList[ops[1]] returns j (var_j)
            # keep in mind that since memory is a dictionary, memory[j] literally goes to when var_j is stored in memory
            # this means that we can simply just read from memory this way!! So smooth!
            #WE ARE UPDATING OUR VARLIST BASED ON A MEMORY LOCATION
            variableList[ops[0]] = memory[variableList[ops[1]]]
        if cmd == "write":
            # ['write', i, j]: store the value of var_j in memory at the location var_i 
            #@deletelater
            # WE ARE UPDATING A MEMORY LOCATION BASED ON OUR VARLIST
            memory[variableList[ops[0]]] = variableList[ops[1]]
            print("written!")
        if cmd == "assign":
            # ['assign', i, j]: assign var_i to the value j
            #@deletelater
            # WE ARE NOT ACTUALLY CHANGING MEMORY, JUST UPDATING A VAR FROM OUR VARLIST WITH ANOTHER VAR ON OUR VARLIST
            #in other words, var_i = var_j
            # TODO: Implement assign.
            #variableList[ops[0]] = variableList[ops[1]]
            print("assigned!")
        # Arithmetic commands
        if cmd == "+":
            # ['+', i, j, k]: compute (var_j + var_k) and store in var_i
            # TODO: Implement addition.
            variableList[ops[0]] = variableList[ops[1]] + variableList[ops[2]]
        if cmd == "-":
            # ['-', i, j, k]: compute max((var_j - var_k), 0) and store in var_i.
            # # TODO: Implement subtraction.
            variableList[ops[0]] = max(variableList[ops[1]] - variableList[ops[2]],0)
            #printState(variableList,memory,inputArr,programArr)
            print("subtracted!")
        if cmd == "*":
            # ['*', i, j, k]: compute (var_j * var_k) and store in var_i.
            # TODO: Implement multiplication.
            variableList[ops[0]] = variableList[ops[1]] * variableList[ops[2]]
        if cmd == "/":
            #  ['/', i, j, k]: compute (var_j // var_k) and store in var_i.
            # Note that this is integer division. You should return an integer, not a float.
            # Remember division by 0 results in 0.
            # TODO: Implement division.
            result = variableList[ops[1]] // variableList[ops[2]]
            variableList[ops[0]] = result if result > 0 else 0
        # Control commands
        if cmd == "goto":
            # ['goto', i, j]: if var_i is equal to 0, go to line j
            # TODO: Implement goto.
            if variableList[ops[0]] == 0:
                programCounter = variableList[ops[1]]
        
        programCounter += 1
    
    # Return the memory starting at output_ptr with length of output_len
    return [memory[i] for i in range(variableList[1], variableList[1]+variableList[2])]
