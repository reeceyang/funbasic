class Fun():
    # FIXME: should args and behavior have default values of None?
    def __init__(self, args, behavior) -> None:
        self.args = args
        self.behavior = behavior
    
    def execute(self):
        return self.behavior.execute()

    # FIXME: should all functions have a to_string implementation?

class VoidFun(Fun):
    def execute(self):
        return self

    def to_string(self):
        return "void"

class TrueFun(Fun):
    def execute(self):
        return self

    def to_string(self):
        return "true"

class FalseFun(Fun):
    def execute(self):
        return self

    def to_string(self):
        return "false"

class NumFun(Fun):
    def __init__(self, args, behavior, value) -> None:
        self.value = value
        super().__init__(args, behavior)

    def execute(self):
        return self

    def to_string(self):
        return str(self.value)

class StringFun(Fun):
    def __init__(self, args, behavior, value) -> None:
        self.value = value
        super().__init__(args, behavior)

    def execute(self):
        return self

    def to_string(self):
        return str(self.value)

class BreakFun():
    def execute(self):
        return self # FIXME: not really sure what this should return

class ContinueFun():
    def execute(self):
        return self  # FIXME: not really sure what this should return

class DoFun(Fun):
    def execute(self):
        for fun in self.args:
            result = fun.execute()
            if isinstance(result, BreakFun) or isinstance(result, ContinueFun):
                return result
        return VoidFun(None, None)

class IfFun(Fun):
    def execute(self):
        if isinstance(self.args[0].execute(), TrueFun):
            return self.args[1].execute()
        return VoidFun(None, None)

class LoopFun(Fun):
    def execute(self):
        while True:
            result = self.args[0].execute()
            if isinstance(result, BreakFun):
                return VoidFun(None, None)
        
class PrintFun(Fun):
    def execute(self):
        for i in range(0, len(self.args) - 1): # FIXME: what if there are no args? same problem for InputFun
            print(self.args[i].execute().to_string(), end=" ")
        if len(self.args) > 0:
            print(self.args[-1].execute().to_string())
        else:
            print()
        return VoidFun(None,None)

class InputFun(Fun):
    def execute(self):
        user_input = None
        for i in range(0, len(self.args) - 1): # FIXME: maybe use print function to avoid code reuse?
            print(self.args[i].execute().to_string(), end=" ")
        if len(self.args) > 0:
            user_input = input(self.args[-1].execute().to_string())
        else:
            user_input = input()
        try:
            float(user_input)
            # user input is a number
            # FIXME: this should be an int if its an int, not a float!
            return NumFun(None,None,float(user_input))
        except ValueError:
            return StringFun(None,None,user_input)
        
var_dict = {}

class PointerFun(Fun):
    def __init__(self, args, behavior, name) -> None:
        self.name = name
        super().__init__(args, behavior)
    
    def execute(self):
        return var_dict[self.name]

class LetFun(Fun):
    def execute(self):
        var_dict[self.args[0]] = self.args[1].execute()
        return var_dict.get(self.args[0])

class PlusFun(Fun):
    def execute(self): # FIXME: PlusFun should be able to have any number of aguments
        return NumFun(None, None, self.args[0].execute().value + self.args[1].execute().value)

class NegateFun(Fun):
    def execute(self):
        return NumFun(None, None, -self.args[0].execute().value)

class MultFun(Fun):
    def execute(self):  # FIXME: MultFun should be able to have any number of aguments
        return NumFun(None, None, self.args[0].execute().value * self.args[1].execute().value)

class DivFun(Fun):
    def execute(self):
        return NumFun(None, None, self.args[0].execute().value / self.args[1].execute().value)

class ModFun(Fun):
    def execute(self):
        return NumFun(None, None, self.args[0].execute().value % self.args[1].execute().value)

class LessFun(Fun):
    def execute(self):
        if self.args[0].execute().value < self.args[1].execute().value:
            return TrueFun(None, None)
        return FalseFun(None, None)

class GreatFun(Fun):
    def execute(self):
        if self.args[0].execute().value > self.args[1].execute().value:
            return TrueFun(None, None)
        return FalseFun(None, None)

class LessEqFun(Fun):
    def execute(self):
        if self.args[0].execute().value <= self.args[1].execute().value:
            return TrueFun(None, None)
        return FalseFun(None, None)

class GreatEqFun(Fun):
    def execute(self):
        if self.args[0].execute().value >= self.args[1].execute().value:
            return TrueFun(None, None)
        return FalseFun(None, None)

class EqFun(Fun): # FIXME: only for numbers right now!
    def execute(self):
        if self.args[0].execute().value == self.args[1].execute().value:
            return TrueFun(None, None)
        return FalseFun(None, None) 

class AndFun(Fun):
    def execute(self):
        if isinstance(self.args[0].execute().value, TrueFun) and isinstance(self.args[0].execute().value, TrueFun):
            return TrueFun(None, None)
        return FalseFun(None, None)

class OrFun(Fun):
    def execute(self):
        if isinstance(self.args[0].execute().value, TrueFun) or isinstance(self.args[0].execute().value, TrueFun):
            return TrueFun(None, None)
        return FalseFun(None, None)

class NotFun(Fun):
    def execute(self):
        if isinstance(self.args[0].execute().value, FalseFun):
            return TrueFun(None, None)
        return FalseFun(None, None)

main = DoFun([],None)
tokens = []
def tokenize(s):
    s = s.strip() + " "
    tokenstart = 0
    for i in range(len(s)):
        if s[i].isspace():
            tokens.append(s[tokenstart:i])
            tokenstart = i + 1
        if s[i] == "(" or s[i] == ")":
            tokens.append(s[tokenstart:i])
            tokens.append(s[i])
            tokenstart = i + 1
    for i in range(len(tokens) - 1, 0, -1):
        if tokens[i] == "":
            tokens.pop(i)
# do, if, loop, break, continue, let, fun, args, return, print, input, +, -, *, /, %, =, >, <, >=, <=, and, not, or, true, false

def build_fun(start):
    i = start
    token = tokens[i]
    while token != "(":
        print("token list:", tokens)
        print("token:",token)
        if token == "(":
            fun.args.append(build_fun(i+1))
        elif token == ")":
            return main
        elif token == "do":
            fun = DoFun([], None)
        elif token == "if":
            fun = IfFun([], None)
        elif token == "loop":
            fun = LoopFun([], None)
        elif token == "break":
            fun = BreakFun([], None)
        elif token == "continue":
            fun = ContinueFun([], None)
        elif token == "let":
            fun = LetFun([], None)
        elif token == "print":
            fun = PrintFun([], None)
        elif token == "input":
            fun = InputFun([], None)
        elif token == "+":
            fun = PlusFun([], None)
        elif token == "-":
            fun = NegateFun([], None)
        elif token == "*":
            fun = MultFun([], None)
        elif token == "/":
            fun = DivFun([], None)
        elif token == "%":
            fun = ModFun([], None)
        elif token == "=":
            fun = EqFun([], None)
        elif token == ">":
            fun = GreatFun([], None)
        elif token == "<":
            fun = LessFun([], None)
        elif token == ">=":
            fun = GreatEqFun([], None)
        elif token == "<=":
            fun = LessEqFun([], None)
        elif token == "and":
            fun = AndFun([], None)
        elif token == "or":
            fun = OrFun([], None)
        elif token == "not":
            fun = NotFun([], None)
        elif token == "true":
            fun = TrueFun([], None)
        elif token == "false":
            fun = FalseFun([], None)
    print("adding",fun)
    main.args.append(fun)
    tokens.pop(i)
    print("missing )")


# tokenize("""let(n input)
# if(or(=(%(n 2) 0) =(%(n 3) 0) do(print(false) break))
# let(p 5)
# loop(
#     if(or(%(n p) >(*(p p) n) do(print(false) break))
#     let(p +(p 2))
# )
# print(true)""")
tokenize("print(false())")
f = build_fun(0)
print(f.args)
#f.execute()

# d = DoFun([LetFun(["a", InputFun([], None)], None), LetFun(["b", InputFun([], None)], None),
#           PrintFun([PlusFun([PointerFun(None, None, "a"), PointerFun(None, None, "b")], None)], None),
#           PrintFun([NegateFun([PointerFun(None, None, "b")], None)], None)], None)
          
# d.execute()
