from collections import defaultdict 

class Calculator():

    def suma(self, a, b):
        res = 0
        for arg in args:
            res += arg
        return res

    def subtract(self, a, b):
        return a - b

    def multiply(self, a,b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return None
        return a / b


if __name__ == "__main__":
    calculator = Calculator()
    operations = {
    "/": lambda a, b: calculator.divide(a, b),
    "*": lambda a, b: calculator.multiply(a, b),
    "+": lambda a, b: calculator.suma(a, b),
    "-": lambda a, b: calculator.subtract(a, b),
    }
    
    usr_input = ""
    valid_operations = "<<param a> (+, -, *, /) <param b>> or 'exit'\n"
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
        args_str = usr_input.split(op)
        if len(args_str) != 2:
            print(f"Sorry, we need 2 (and only 2) arguments to perform the operation")
            continue
        
        ## convert to numbers
        try:
            print(args_str)
            args = [float(arg) for arg in args_str]    
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
   
    
    