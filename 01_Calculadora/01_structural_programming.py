
def divide(a, b):
    if b == 0:
        return None
    return a / b

operations = {
    "/": lambda a, b: divide(a, b),
    "*": lambda a, b: a * b,
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "hex": lambda a, b: hex(a)
}

if __name__ == "__main__":
    usr_input = ""
    valid_operations = "<(+, -, *, /, hex)> or 'exit'\n"
    results = []
    while True:
        usr_input = input(f"Please enter your operation to calculate: {valid_operations}")
        
        ## remove spaces
        usr_input = usr_input.replace(" ", "")
        
        if "exit" in usr_input:
            print(f"Thanks for using our services. See you soon!")
            break
        
        ## Validate supported operations
        ops = [op for op in operations.keys() if op in usr_input]
        if len(ops)==0:
            print(f"Sorry, operation not supported. Please only enter {valid_operations}")
            continue
        
       ## atm with only a single operation
        op = ops[0]
        args_str = [i for i in usr_input.split(op) if i!=""]
        # if op != "hex" and len(args_str) != 2:
        #     print(f"Sorry, we need 2 (and only 2) arguments to perform the operation {op}")
        #     continue
        # elif len(args_str) != 1:
        #     print(f"Sorry, we need 1 (and only 1) arguments to perform the operation {op}")
        #     continue
        
        try:
            if op != "hex":
                args = [float(arg) for arg in args_str]
            else: 
                args = [int(args_str[0]), None]
        except ValueError:
            print(f"Sorry, we could't convert all the arguments to numbers")
            continue
        a, b = args
        
        ## perform operation
        result = operations[op](a, b)
        
        if result is None and op == "/":
            print("Not possible to divide by zero")
            continue
        
        print(f"Operation Success: the result from {usr_input} is {result}")
        
        results.append(result)
        
        print(f"Last Operations =")
        for res in results:
            print(res)
        
        
   
    
    