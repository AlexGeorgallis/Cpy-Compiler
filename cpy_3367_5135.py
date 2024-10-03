# Konstantinos  Christodoulou   3367
# Alexandros    Georgalli       5135

import string
import sys

global intermediate_code_list
global intermediate_code_list2
global counter
global quad_label
global scope_list
global scope_count
global is_argument
global is_global
global final_count


line = 1
pos = 0
L = []
token_index = 0


intermediate_code_list = []
intermediate_code_list2 = []
scope_list = []
quad_label = 100
counter = 0
scope_count = 0
final_count = 0
is_argument = False
is_global = False

reserved_words = ['main', 'def', '#def', '#int', 'int', 'global', 'if', 'elif',
                  'else', 'while', 'print', 'return', 'input', 'and', 'or', 'not']

latin_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return f"{self.recognized_string}, family: {self.family}, line: {self.line_number}"


# LEXER #
def next_token(file_name):

    global line, pos

    with open(file_name, "r") as f:
        ##### f.seek(pos)
        state = 0
        token = ''

        while True:  # while state != 13
            f.seek(pos) #####
            c = f.read(1)

            if state == 0 and c in string.whitespace and c != '':
                pos = f.tell()
                # print("pos = ", pos)
                if c == '\n':
                    line += 1

            elif state == 0 and c in latin_alphabet:
                pos += 1 #####
                state = 1
                token += c

            elif state == 1 and (c in latin_alphabet or c.isdigit()):
                pos += 1 #####
                token += c

            elif state == 1 and not c.isdigit() and c not in latin_alphabet:
                ##### pos = f.tell() - 1
                if len(token) > 30:
                    token = token[:30]
                if token in reserved_words:
                    return Token(token, "keyword", line)
                else:
                    return Token(token, "identifier", line)

            elif state == 0 and c.isdigit():
                pos += 1 #####
                state = 2
                token += c

            elif state == 2 and c.isdigit():
                pos += 1 #####
                token += c

            elif state == 2 and (not c.isdigit()):
                if c in latin_alphabet:
                    print("Illegal argument at line", line, ": Digit as first character of identifier")
                    sys.exit(1)
                ##### pos = f.tell() - 1
                if -32767 <= int(token) <= 32767:
                    return Token(token, "number", line)
                else:
                    print("out-of-bounds number", token, "[-32767, 32767]")
                    sys.exit(2)

            elif state == 0 and c == '+':
                pos += 1
                return Token(c, "addOperator", line)

            elif state == 0 and c == '-':
                pos += 1
                return Token(c, "addOperator", line)

            elif state == 0 and c == '*':
                pos += 1
                return Token(c, "mulOperator", line)

            elif state == 0 and c == '%':
                pos += 1
                return Token(c, "mulOperator", line)

            elif state == 0 and c == ',':
                pos += 1
                return Token(c, "delimiter", line)

            elif state == 0 and c == ':':
                pos += 1
                return Token(c, "delimiter", line)

            elif state == 0 and c == '(':
                pos += 1
                return Token(c, "delimiter", line)

            elif state == 0 and c == ')':
                pos += 1
                return Token(c, "delimiter", line)

            elif state == 0 and c == '<':
                pos += 1 #####
                state = 3

            elif state == 3 and c == '=':
                pos += 1 ##### pos = f.tell()
                return Token('<=', "relOperator", line)

            elif state == 3 and c != '=':
                ##### pos = f.tell() - 1
                return Token('<', "relOperator", line)

            elif state == 0 and c == '>':
                pos += 1 #####
                state = 4

            elif state == 4 and c == '=':
                pos += 1 ##### pos = f.tell()
                return Token('>=', "relOperator", line)

            elif state == 4 and c != '=':
                ##### pos = f.tell() - 1
                return Token('>', "relOperator", line)

            elif state == 0 and c == '=':
                pos += 1 ######
                state = 5

            elif state == 5 and c == '=':
                pos += 1 ##### pos = f.tell()
                return Token('==', "relOperator", line)

            elif state == 5 and c != '=':
                ###### pos = f.tell() - 1
                return Token('=', "assignment", line)

            elif state == 0 and c == '/':
                pos += 1 ######
                state = 6

            elif state == 6 and c == '/':
                pos += 1 ##### pos = f.tell()
                return Token('//', "mulOperator", line)

            elif state == 6 and c != '/':
                token = '/' + c
                print("Invalid token", token, "encountered at line", line)
                sys.exit(1)

            elif state == 0 and c == '!':
                pos += 1 ######
                state = 7

            elif state == 7 and c == '=':
                pos += 1 ##### pos = f.tell()
                return Token('!=', "relOperator", line)

            elif state == 7 and c != '=':
                token = '!' + c
                print("Invalid token", token, "encountered at line", line)
                sys.exit(1)

            elif state == 0 and c == '#':
                pos += 1 ######
                state = 8

            elif state == 8 and c == '#':
                pos += 1 ######
                state = 9

            elif state == 9 and c != '#':
                if not c:
                    print("Error at line:", line, "Opened comments without closing!")
                    sys.exit(1)
                pos += 1 #####
                pass


            elif state == 9 and c == '#':
                pos += 1 ######
                state = 10

            elif state == 10 and c == '#':
                pos += 1 ######
                state = 0

            elif state == 10 and c != '#':
                pos += 1 ######
                state = 9

            elif state == 8 and c == '{':
                pos += 1 ##### pos = f.tell()
                return Token('#{', "groupSymbol", line)

            elif state == 8 and c == '}':
                pos += 1 ##### pos = f.tell()
                return Token('#}', "groupSymbol", line)

            elif state == 8 and c == 'd':
                token += '#'
                token += c
                c = f.read(1)
                if c == 'e':
                    token += c
                    c = f.read(1)
                    if c == 'f':
                        token += c
                        c = f.read(1)
                        token += c
                        if c.isspace():
                            pos += 3 #####pos = f.tell()
                            return Token('#def', "keyword", line)

                        else:
                            print("Invalid token", token, "encountered at line", line)
                            sys.exit(1)

            elif state == 8 and c == 'i':
                token += '#'
                token += c
                c = f.read(1)
                if c == 'n':
                    token += c
                    c = f.read(1)
                    if c == 't':
                        token += c
                        c = f.read(1)
                        token += c
                        if c.isspace():
                            pos += 3 ##### pos = f.tell()
                            return Token('#int', "keyword", line)

                        else:
                            print("Invalid token", token, "encountered at line", line)
                            sys.exit(1)

            elif state == 8 and (c != '#' or c != '{' or c != '}' or c != 'd' or c != 'i'):
                token = '#' + c
                print("Invalid token", token, "encountered at line", line)
                sys.exit(1)

            elif state == 0 and not c:
                #print("eof, line:", line)
                break

            else:
                print("Invalid character", c, "encountered at line", line)
                sys.exit(1)


# PARSER #
def syntax_analyzer(tokens):
    global token_index
    global scope_list
    global scope_count
    global is_argument

    def match(expected_token):
        global token_index
        global intermediate_code_list

        if tokens[token_index][0] == expected_token or tokens[token_index][1] == expected_token:
            token_index += 1
            if token_index + 1 > len(tokens):
                calculate_framelength()
                gen_quad('halt', '_', '_', '_')
                gen_quad('end_block', 'main', '_', '_')
                gen_quad('halt', '_', '_', '_')
                add_scope('main')
                delete_scope()
                gen_quad('end_block', 'program', '_', '_')
                add_scope('program')
                delete_scope()
                generate_final()
                write_symbols_to_file(symbol_file)
                write_int_file(intermediate_code_list)
                print("Compilation was successful!")

                main_index = None
                for i in intermediate_code_list:
                    if i[1] == 'begin_block' and i[2] == 'main':
                        main_index = i[0]
                symbol_file.close()
                final_file.close()
                with open('cpy_3367_5135.asm', 'r') as file:
                    content = file.read()
                updated_content = f"j L{main_index}\n" + content
                with open('cpy_3367_5135.asm', 'w') as file:
                    file.write(updated_content)
                final_file.close()

                sys.exit(0)
        else:
            print("Syntax error: Expected", expected_token, "but got", tokens[token_index][0], "line", tokens[token_index][2])
            sys.exit(1)

    def declarations():
        while declaration_line():
            continue

    def declaration_line():
        global is_argument

        if tokens[token_index][0] == '#int':
            match('#int')
            is_argument = False
            id_list()
            return True

        # elif tokens[token_index][1] == 'identifier':
        #     entity = Entity()
        #     assign_entity(entity, tokens[token_index][0], 'VARIABLE', calculate_offset())
        #     add_entity(entity)


        else:
            return False

    def id_list():
        global is_argument

        if is_argument:
            argument = Argument()
            argument.name = tokens[token_index][0]
            add_argument(argument)
        else:
            entity = Entity()
            assign_entity(entity, tokens[token_index][0], 'VARIABLE', calculate_offset())
            add_entity(entity)

        match(tokens[token_index][1])

        while tokens[token_index][0] == ',':
            match(',')
            match(tokens[token_index][1])

            if is_argument:
                argument = Argument()
                argument.name = tokens[token_index-1][0]
                add_argument(argument)
            else:
                entity = Entity()
                assign_entity(entity, tokens[token_index-1][0], 'VARIABLE', calculate_offset())
                add_entity(entity)

    def statement():
        if tokens[token_index][1] == 'identifier':
            assignment_stat()
        elif tokens[token_index][0] == 'print':
            print_stat()
        elif tokens[token_index][0] == 'return':
            return_stat()
        elif tokens[token_index][0] == 'if':
            if_stat()
        elif tokens[token_index][0] == 'while':
            while_stat()
        else:
            return False

    def assignment_stat():
        ID = tokens[token_index][0]
        match('identifier')
        match('=')
        if tokens[token_index][0] == 'int':
            match('int')
            match('(')
            match('input')
            match('(')
            match(')')
            match(')')
            temp = new_temp()

            gen_quad('inp', temp, '_', '_')
            gen_quad('=', temp, '_', ID)
        else:
            E = expression()
            gen_quad('=', E, '_', ID)

    def print_stat():
        match('print')
        match('(')
        E = expression()
        gen_quad('out', E, '_', '_')
        match(')')

    def return_stat():
        match('return')
        E = expression()
        gen_quad('retv', E, '_', '_')

    def if_stat():
        Btrue = []
        Bfalse = []
        if_list = []
        elif_list = []

        match('if')
        B = condition()
        Btrue = B[0]
        Bfalse = B[1]
        backpatch(Btrue, next_quad())
        match(':')
        if tokens[token_index][0] == '#{':
            match('#{')
            statements()
            if_list = make_list(next_quad())
            gen_quad('jump', '_', '_', '_')
            backpatch(Bfalse, next_quad())
            backpatch(if_list, next_quad())
            match('#}')
        else:
            statement()
            if_list = make_list(next_quad())
            gen_quad('jump', '_', '_', '_')
            backpatch(Bfalse, next_quad())
            backpatch(if_list, next_quad())
        while tokens[token_index][0] == 'elif':
            match('elif')
            B = condition()
            Btrue = B[0]
            Bfalse = B[1]
            backpatch(Btrue, next_quad())
            match(':')
            if tokens[token_index][0] == '#{':
                match('#{')
                statements()
                elif_list = make_list(next_quad())
                gen_quad('jump', '_', '_', '_')
                backpatch(Bfalse, next_quad())
                match('#}')
            else:
                statement()
                elif_list = make_list(next_quad())
                gen_quad('jump', '_', '_', '_')
                backpatch(Bfalse, next_quad())
                backpatch(if_list, next_quad())

        if tokens[token_index][0] == 'else':
            match('else')
            match(':')
            if tokens[token_index][0] == '#{':
                match('#{')
                statements()
                backpatch(if_list, next_quad())
                backpatch(elif_list, next_quad())
                match('#}')
            else:
                statement()
                backpatch(if_list, next_quad())
                backpatch(elif_list, next_quad())


    def while_stat():
        Btrue = []
        Bfalse = []

        match('while')
        Bquad = next_quad()
        B = condition()
        Btrue = B[0]
        Bfalse = B[1]
        backpatch(Btrue, next_quad())
        match(':')
        if tokens[token_index][0] == '#{':
            match('#{')
            statements()
            gen_quad('jump', '_', '_', Bquad)
            backpatch(Bfalse, next_quad())
            match('#}')
        else:
            statement()
            gen_quad('jump', '_', '_', Bquad)
            backpatch(Bfalse, next_quad())

    def expression():
        opt_sign = optional_sign()
        if opt_sign:
            w = new_temp()
            T1 = term()
            gen_quad(opt_sign, 0, T1, w)
            E = w
            return E
        else:
            T1 = term()
        while tokens[token_index][1] == 'addOperator':
            op = tokens[token_index][0]
            match('addOperator')
            T2 = term()
            w = new_temp()
            gen_quad(op, T1, T2, w)
            T1 = w
        E = T1

        return E

    def term():
        F1 = factor()
        while tokens[token_index][1] == 'mulOperator':
            op = tokens[token_index][0]
            match(tokens[token_index][0])
            F2 = factor()
            w = new_temp()
            gen_quad(op, F1, F2, w)
            F1 = w
        T = F1
        return T

    def factor():
        if tokens[token_index][1] == 'number':
            F = tokens[token_index][0]
            match('number')
        elif tokens[token_index][0] == '(':
            match('(')
            E = expression()
            match(')')
            F = E
        elif tokens[token_index][1] == 'identifier':
            id = tokens[token_index][0]
            match('identifier')
            F = idtail(id)
        else:
            print("Syntax error: Invalid factor")
            sys.exit(1)
        return F

    def idtail(function_name):
        if tokens[token_index][0] == '(':
            match('(')
            w = new_temp()
            if tokens[token_index][0] == ')':
                gen_quad('par', w, 'RET', '_')
                gen_quad('call', function_name, '_', '_')
                match(')')
                return w
            else:
                actual_par_list()
                gen_quad('par', w, 'RET', '_')
                gen_quad('call', function_name, '_', '_')
                match(')')
                return w
        return function_name

    def actual_par_list():
        E = expression()
        gen_quad('par', E, 'CV', '_')
        while tokens[token_index][0] == ',':
            match(',')
            E = expression()
            gen_quad('par', E, 'CV', '_')

    def optional_sign():

        if tokens[token_index][1] == 'addOperator':
            op = tokens[token_index][0]
            match(tokens[token_index][0])

            return op

    def condition():
        Btrue = []
        Bfalse = []
        Q1 = bool_term()
        Q1true = Q1[0]
        Q1false = Q1[1]
        Btrue = Q1true
        Bfalse = Q1false

        while tokens[token_index][0] == 'or':
            backpatch(Q1false, next_quad())
            match('or')
            Q2 = bool_term()
            Q2true = Q2[0]
            Q2false = Q2[1]
            Btrue = merge_list(Q1true, Q2true)
            Bfalse = Q2false

        return Btrue, Bfalse

    def bool_term():
        Btrue = []
        Bfalse = []

        B1 = bool_factor()
        Qtrue = B1[0]
        Qfalse = B1[1]
        Btrue = Qtrue
        Bfalse = Qfalse

        while tokens[token_index][0] == 'and':
            backpatch(Qtrue, next_quad())
            match('and')
            B2 = bool_factor()
            Q2true = B2[0]
            Q2false = B2[1]
            Qfalse = merge_list(Qfalse, Q2false)
            Qtrue = Q2true
            Btrue = Qtrue
            Bfalse = Qfalse

        return Btrue, Bfalse

    def bool_factor():
        Btrue = []
        Bfalse = []

        if tokens[token_index][0] == 'not':
            match('not')
            R = condition()
            Rtrue = R[0]
            Rfalse = R[1]
            Btrue = Rtrue
            Bfalse = Rfalse

        else:
            E1 = expression()
            rel_op = tokens[token_index][0]
            match('relOperator')
            E2 = expression()
            Rtrue = make_list(next_quad())
            gen_quad(rel_op, E1, E2, '_')
            Rfalse = make_list(next_quad())
            gen_quad('jump', '_', '_', '_')
            Btrue = Rtrue
            Bfalse = Rfalse

        return Btrue, Bfalse

    def def_main():
        global is_argument
        match('#def')
        match('main')
        entity = Entity()
        entity.datatype = 'FUNCTION'
        entity.name = 'main'
        entity.function.nesting_level = scope_list[-1].nesting_level + 1
        add_entity(entity)
        add_scope('main')
        is_argument = False
        calculate_starting_quad()
        gen_quad('begin_block', 'main', '_', '_')
        declarations()
        statement()
        #if tokens[token_index][1] == 'identifier':
            #entity = Entity()
            #assign_entity(entity, tokens[token_index][0], 'VARIABLE', calculate_offset())
            #add_entity(entity)
        while True:
            statement()
            #if tokens[token_index][1] == 'identifier':
                #entity = Entity()
                #assign_entity(entity, tokens[token_index][0], 'VARIABLE', calculate_offset())
                #add_entity(entity)

    def def_function():
        global token_index
        global scope_list
        global is_argument

        match('def')
        ID = tokens[token_index][0]
        match('identifier')
        entity = Entity()
        entity.datatype = 'FUNCTION'
        entity.name = ID
        entity.function.nesting_level = scope_list[-1].nesting_level + 1
        add_entity(entity)
        match('(')
        is_argument = True
        id_list()
        match(')')
        match(':')
        match("#{")
        add_scope(ID)
        add_parameters()
        declarations()
        while tokens[token_index][0] == 'def':
            def_function()
        calculate_starting_quad()
        is_argument = False
        gen_quad('begin_block', ID, '_', '_')
        def_globals()
        while True:
            statements()
            if not statements():
                break
        match('#}')
        calculate_framelength()
        gen_quad('end_block', ID, '_', '_')
        write_symbols_to_file(symbol_file)
        add_scope(ID)
        delete_scope()

    def def_globals():
        while global_line():
            continue

    def global_line():
        global is_argument
        global is_global
        if tokens[token_index][0] == 'global':
            match('global')
            is_argument = False
            is_global = True
            id_list()
            return True
        return False

    def statements():
        statement()
        while True:
            if not statement():
                break
            statement()

    def start_rule():
        add_scope('program')
        gen_quad('begin_block', 'program', '_', '_')
        declarations()
        while tokens[token_index][0] == 'def':
            def_function()
        def_main()
        match('eof')

    start_rule()

    if token_index != len(tokens):
        print(tokens[token_index][0], tokens[token_index][2])
        print("Syntax error: Unexpected tokens at the end of the program")
        sys.exit(1)


# HELPER FUNCTIONS FOR INTERMEDIATE CODE #
def next_quad():
    global intermediate_code_list2
    global quad_label
    return quad_label


def new_temp():
    global counter
    global intermediate_code_list2
    counter += 1
    entity = Entity()
    assign_entity(entity, 'T_' + str(counter), 'TEMPORARYVARIABLE', calculate_offset())
    add_entity(entity)

    return f"T_{counter}"


def gen_quad(op, x, y, z):
    global quad_label
    global intermediate_code_list
    global intermediate_code_list2
    my_list = []
    my_list.insert(0, next_quad())
    my_list.insert(1, str(op))
    my_list.insert(2, str(x))
    my_list.insert(3, str(y))
    my_list.insert(4, str(z))

    intermediate_code_list.append(my_list)
    intermediate_code_list2.append(my_list)
    quad_label += 1

    return my_list


def empty_list():
    return []


def make_list(label):
    return [label]


def merge_list(list1, list2):
    return list1 + list2


def backpatch(my_list, label):
    global intermediate_code_list
    my_list.sort()
    x = 0
    count = 0

    for i in my_list:
        for j in intermediate_code_list[x:]:
            if j[0] == i:
                j[4] = str(label)
                count += 1
                x = count
                break
            else:
                count += 1
        count = 0


def write_int_file(input_list):
    with open('cpy_3367_5135.int', 'w') as file:
        for quad in input_list:
            file.write(f"{quad[0]}: {quad[1]}, {quad[2]}, {quad[3]}, {quad[4]}\n")


# SYMBOL TABLE

class Scope():
    def __init__(self):
        self.name = ''
        self.entity_list = []
        self.nesting_level = 0


class Entity():
    def __init__(self):
        self.name = ''
        self.datatype = ''
        self.variable = self.Variable()
        self.function = self.Function()
        self.parameter = self.Parameter()
        self.temp_var = self.TemporaryVariable()

    class Variable():
        def __init__(self):
            self.offset = 0

    class Function():
        def __init__(self):
            self.starting_quad = 0
            self.frame_length = 0
            self.argument_list = []
            self.nesting_level = 0

    class Parameter():
        def __init__(self):
            self.offset = 0

    class TemporaryVariable():
        def __init__(self):
            self.offset = 0


class Argument():
    def __init__(self):
        self.name = ''


def add_entity(entity):
    global scope_list
    scope_list[-1].entity_list += [entity]


scope_count = 0
def nesting_level_assign(scope):
    global scope_count
    scope.nesting_level = scope_count


def add_argument(argument):
    global scope_list
    scope_list[-1].entity_list[-1].function.argument_list += [argument]


def add_scope(name):
    global scope_list
    global scope_count

    next_scope = Scope()
    next_scope.name = name
    if len(scope_list) >= 1:
        scope_count += 1
        nesting_level_assign(next_scope)

    scope_list.append(next_scope)


def delete_scope():
    global scope_list
    global scope_count
    scope_count = 0

    for i in range(len(scope_list[-1].entity_list)):
        scope_list[-1].entity_list.pop()

    del scope_list[-1]


def calculate_offset():
    global scope_list
    offset = 12

    if len(scope_list[-1].entity_list) >= 1:
        for i in range(len(scope_list[-1].entity_list)):
            if scope_list[-1].entity_list[i].datatype == 'VARIABLE' or scope_list[-1].entity_list[i].datatype == 'TEMPORARYVARIABLE' or scope_list[-1].entity_list[i].datatype == 'PARAMETER':
                offset += 4

    return offset


def calculate_framelength():
    global scope_list
    scope_list[-2].entity_list[-1].function.frame_length = calculate_offset()


def calculate_starting_quad():
    global scope_list
    scope_list[-2].entity_list[-1].function.starting_quad = next_quad()


def find_entity(v_name):
    global scope_list
    for scope in scope_list:
        for entity in scope.entity_list:
            if entity.name == v_name:
                v = entity
                entity_scope = scope
                return entity_scope, v
            else:
                continue

    else:
        print(f"Entity with name {v_name} does not exist")
        sys.exit(0)


def assign_entity(ent, name, type, offset):
    ent.name = name
    ent.datatype = type
    if ent.datatype == 'PARAMETER':
        ent.parameter.offset = offset

    elif ent.datatype == 'VARIABLE':
        ent.variable.offset = offset

    elif ent.datatype == 'TEMPORARYVARIABLE':
        ent.temp_var.offset = offset


def add_parameters():
    global scope_list

    for i in scope_list[-2].entity_list[-1].function.argument_list:
        entity = Entity()
        assign_entity(entity, i.name, 'PARAMETER', calculate_offset())
        add_entity(entity)


def write_symbols_to_file(file):
    global scope_list
    file.write('-'*100)
    file.write('\n')

    for i in scope_list:
        file.write('\n')
        file.write('Scope: ' + str(i.name) + ' ' + 'nesting_level: ' + str(i.nesting_level))

        for j in i.entity_list:
            file.write('\n')
            file.write('\tEntity: ' + str(j.name) + ' ' + str(j.datatype))
            file.write('\n')

            if j.datatype == 'VARIABLE':
                file.write('\tOffset: ' + str(j.variable.offset))
                file.write('\n')

            elif j.datatype == 'PARAMETER':
                file.write('\tOffset: ' + str(j.parameter.offset))
                file.write('\n')

            elif j.datatype == 'TEMPORARYVARIABLE':
                file.write('\tOffset: ' + str(j.temp_var.offset))
                file.write('\n')

            elif j.datatype == 'FUNCTION':
                file.write('\tFramelength of function ' + str(j.name) + ': ' + str(j.function.frame_length))
                file.write('\n')
                file.write('\tStarting_quad of function ' + str(j.name) + ': ' + str(j.function.starting_quad))
                file.write('\n')

                for k in j.function.argument_list:
                    file.write('\tArgument: ' + str(k.name))
                    file.write('\n')


## TARGET CODE ##

def gnlvcode(v_name):
    global scope_count
    global scope_list

    # Find the entity and it's scope
    for scope in scope_list:
        for entity in scope.entity_list:
            if entity.name == v_name:
                v = entity
                entity_scope = scope
                break
        else:
            continue
        break
    else:
        print(f"Entity with name {v_name} does not exist")
        sys.exit(0)

    # Generate RISC-V code
    returning_riscv_code = 'lw t0,-4(sp)\n'
    x = scope_count
    i = entity_scope.nesting_level

    while x > i:
        returning_riscv_code += 'lw t0, -4(t0)\n'
        x -= 1

    if v.datatype == 'VARIABLE':
        offset = v.variable.offset
    elif v.datatype == 'PARAMETER':
        offset = v.parameter.offset
    elif v.datatype == 'TEMPORARYVARIABLE':
        offset = v.temp_var.offset
    else:
        print(f"Entity with name {v_name} has an unsupported datatype {v.datatype}")
        sys.exit(0)

    returning_riscv_code += f'addi t0, t0, -{offset}\n'
    return returning_riscv_code


def loadvr(v_name, reg):
    if v_name.isdigit():
        final_file.write('li t%s, %s\n' % (reg, v_name))

    else:
        # Find the entity and its scope
        for scope in scope_list:
            for entity in scope.entity_list:
                if entity.name == v_name:
                    v = entity
                    entity_scope = scope
                    break
            else:
                continue
            break
        else:
            print(f"Entity with name {v_name} does not exist")
            sys.exit(0)
        if entity_scope.nesting_level == 0:
            if v.datatype == 'VARIABLE':
                final_file.write('lw t%s, -%d(gp)\n' % (reg, v.variable.offset))
            elif v.datatype == 'TEMPORARYVARIABLE':
                final_file.write('lw t%s, -%d(gp)\n' % (reg, v.temp_var.offset))

        elif entity_scope.nesting_level == scope_list[-1].nesting_level:
            if v.datatype == 'VARIABLE':
                final_file.write('lw t%s, -%d(sp)\n' % (reg, v.variable.offset))
            elif v.datatype == 'TEMPORARYVARIABLE':
                final_file.write('lw t%s, -%d(sp)\n' % (reg, v.temp_var.offset))
            elif v.datatype == 'PARAMETER':
                final_file.write('lw t%s, -%d(sp)\n' % (reg, v.parameter.offset))

        elif entity_scope.nesting_level < scope_list[-1].nesting_level:
            if v.datatype == 'VARIABLE':
                gnlvcode(v_name)
                final_file.write('lw t%s, (t0)\n' % reg)
            elif v.datatype == 'PARAMETER':
                gnlvcode(v_name)
                final_file.write('lw t%s, (t0)\n' % reg)


def storerv(reg, v_name):
    (scope, entity) = find_entity(v_name)
    if scope.nesting_level == 0:
        if entity.datatype == 'VARIABLE':
            final_file.write('sw t%d, -%d(gp)\n' % (reg, entity.variable.offset))
        elif entity.datatype == 'TEMPORARYVARIABLE':
            final_file.write('sw t%d, -%d(gp)\n' % (reg, entity.temp_var.offset))

    elif scope.nesting_level == scope_list[-1].nesting_level:
        if entity.datatype == 'VARIABLE':
            final_file.write('sw t%d, -%d(sp)\n' % (reg, entity.variable.offset))
        elif entity.datatype == 'TEMPORARYVARIABLE':
            final_file.write('sw t%d, -%d(sp)\n' % (reg, entity.temp_var.offset))
        elif entity.datatype == 'PARAMETER':
            final_file.write('sw t%d, -%d(sp)\n' % (reg, entity.parameter.offset))

    elif scope.nesting_level < scope_list[-1].nesting_level:
        if entity.datatype == 'VARIABLE':
            gnlvcode(v_name)
            final_file.write('sw t%d, (t0)\n' % reg)
        elif entity.datatype == 'PARAMETER':
            gnlvcode(v_name)
            final_file.write('sw t%d, (t0)\n' % reg)


def generate_final():
    global scope_list
    global intermediate_code_list
    global intermediate_code_list2
    global final_count

    relop_ops = ['==', '!=', '<', '<=', '>', '>=']
    assembly_ops = ['beq', 'bne', 'blt', 'ble', 'bgt', 'bge']
    num_ops = ['+', '-', '*', '//', '%']
    assembly_arithmetic_ops = ['add', 'sub', 'mul', 'div', 'div']
    final_flag = 0

    for i in intermediate_code_list:
        final_file.write('L' + str(i[0]) + ': \n')
        if i[1] == 'jump':
            final_file.write('j L' + str(i[4]) + '\n')
        elif i[1] in relop_ops:
            x = assembly_ops[relop_ops.index(i[1])]
            loadvr(i[2], 1)
            loadvr(i[3], 2)
            final_file.write(x + ' , t1, t2, L' + i[4] + '\n')
        elif i[1] in num_ops:
            x = assembly_arithmetic_ops[num_ops.index(i[1])]
            loadvr(i[2], 1)
            loadvr(i[3], 2)
            final_file.write(x + ' ,t1, t1, t2\n')
            storerv(1, i[4])
        elif i[1] == '=':
            loadvr(i[2], 1)
            storerv(1, i[4])
        elif i[1] == 'retv':
            loadvr(i[2], 1)
            final_file.write('lw t0, -8(sp)\n')
            final_file.write('sw t1, 0(t0)\n')
            final_file.write('lw ra, 0(sp)\n')
            final_file.write('jr ra\n')
        elif i[1] == 'inp':
            final_file.write('li a7, 5\n')
            final_file.write('ecall\n')
            final_file.write('mv t1, a0\n')
            storerv(1, i[2])
        elif i[1] == 'out':
            loadvr(i[2], 1)
            final_file.write('mv a0, t1\n')
            final_file.write('li a7, 1\n')
            final_file.write('ecall\n')
        elif i[1] == 'halt':
            final_file.write('li a0, 0\n')
            final_file.write('li a7, 10\n')
            final_file.write('ecall\n')
        elif i[1] == 'begin_block' and scope_list[-1].nesting_level != 0:
            final_file.write('sw ra, (sp)\n')
        elif i[1] == 'end_block' and scope_list[-1].nesting_level != 0:
            final_file.write('lw ra, (sp)\n')
            final_file.write('jr ra\n')
        elif i[1] == 'begin_block' and i[1] == scope_list[-1].nesting_level == 0:
            final_file.seek(0, 0)
            final_file.write('j L%d\n' % i[0])
            final_file.seek(0, 2)
            final_file.write('addi sp, sp, %d\n' % calculate_offset())
            final_file.write('mv gp, sp\n')
        elif i[1] == 'par':
            j = intermediate_code_list.index(i)
            for k in intermediate_code_list[j:]:
                if k[1] == 'call' and final_flag == 0:
                    (scope, entity) = find_entity(k[2])
                    final_file.write('addi fp, sp, %d\n' % entity.function.frame_length)
                    final_flag = 1
                    break
            if i[3] == 'CV':
                loadvr(i[2], 0)
                final_file.write('sw t0, -%d(fp)\n' % (12 + 4 * final_count))
                final_count += 1
            elif i[3] == 'RET':
                (scope, entity) = find_entity(i[2])
                final_file.write('addi t0, sp, -%d\n' % entity.temp_var.offset)
                final_file.write('sw t0, -8(sp)\n')
        elif i[1] == 'call':
            final_flag = 0
            final_count = 0
            (scope, entity) = find_entity(i[2])
            if scope_list[-1].nesting_level < entity.function.nesting_level:
                final_file.write('sw sp, -4(fp)\n')
            elif scope_list[-1].nesting_level == entity.function.nesting_level:
                final_file.write('lw t0, -4(sp)\n')
                final_file.write('sw t0, -4(fp)\n')
            final_file.write('addi sp, sp, %d\n' % entity.function.frame_length)
            final_file.write('jal L%d\n' % entity.function.starting_quad)
            final_file.write('addi sp, sp, -%d\n' % entity.function.frame_length)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(3)
    input_file = sys.argv[1]
    symbol_file = open('cpy_3367_5135.sym', 'w')
    final_file = open('cpy_3367_5135.asm', 'w')
    final_file.write('\n')

    while True:
        tk = next_token(input_file)
        if not tk:
            break
        L.append([tk.recognized_string, tk.family, tk.line_number])
    syntax_analyzer(L)