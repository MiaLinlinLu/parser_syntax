######################################################################################################
###  Usage.
# read from "program.txt",


# if there is lexical error,
# it will print analzed TOKENS and "LEXICAL ERROR DETECTED".

# If there is no lexical error,
# it will print TOKENs
# if no syntax error, "No Syntax Error"
# if syntax error, "Error Detected"

######################################################################################################
"""
lexical analyzer 
"""

# define DELIMITER
def isDelimiter(ch):
    this_s = " +-=*/><(){;}=%"
    if ch in list(this_s) + ["\t", "\n"]:
        return True
    return False


# define OPERATOR
def isMathOperator(ch):
    this_s = "+-/*%"
    if ch in list(this_s):
        return True
    return False


# define BOOL OPERATOR
def isBoolOperator(ch):
    if ch in [">", "<"]:
        return True
    return False


# valid IDENTIFIER
def is_valid_identifier(s):
    this_s = "0123456789+-=*/><()[,]{;}"
    if s[0] in list(this_s):
        return False
    return True


# OCTAL NUMBERS
def is_octal(s):
    if not s:
        return False
    if len(s) > 1 and s[0] == "0":
        for digit in s[1:]:
            if digit not in ["0", "1", "2", "3", "4", "5", "6", "7"]:
                return False
        return True
    return False


# HEX NUMBERS
def is_hex(s):
    this_s = "0123456789abcdefABCDEF"
    if len(s) > 2:
        if s[:2] in ["0X", "0x"]:
            for digit in s[2:]:
                if digit not in list(this_s):
                    return False
            return True
    return False


# INTEGER
def is_integer(s):
    if not s:
        return False
    this_s1 = "123456789"
    this_s = "0123456789"

    # Other numbers
    if s[0] in list(this_s1):
        if len(s) > 1:
            for i in s[1:]:
                if i not in list(this_s):
                    return False
            return True
        if len(s) == 1:
            return True
    if s[0] == "-":
        if len(s) == 1:
            return False
        else:
            for i in s[1:]:
                if i not in list(this_s):
                    return False
            return True
    return False


# FLOAT NUMBER
def is_float(s):
    n = len(s)
    flag = 0
    this_s = "0123456789."
    if not n:
        return False
    for i in range(n):
        if (s[i] not in list(this_s)) or (s[i] == "-" and i > 0):
            return False
        if s[i] == ".":
            flag += 1
    if flag == 1:
        return True
    return False


# PARSING STRING
elements = [
    "(",
    ")",
    "{",
    "}",
    ";",
    "=",
    "IF_CODE",
    "ELSE_CODE",
    "FLOAT",
    "INTEGER",
    "MATH_OPERATOR",
    "BOOL_OPERATOR",
    "SWITCH_CODE",
    "CASE_CODE",
    "FOREACH_CODE" "RETURN_CODE",
    "DO_CODE",
    "WHILE_CODE",
    "VOIDMAIN_CODE",
]

key_words_dic = {
    "if": "IF_CODE",
    "else": "ELSE_CODE",
    "switch": "SWITCH_CODE",
    "case": "CASE_CODE",
    "foreach": "FOREACH_CODE",
    "return": "RETURN_CODE",
    "do": "DO_CODE",
    "for": "FOR_CODE",
    "while": "WHILE_CODE",
    "VOID": "VOID_CODE",
    "MAIN": "MAIN_CODE",
}


def lexical_error():
    print("LEXICAL ERROR DETECTED.")


def lexical_parse(s):
    """
    return RESULT:[] --> a list of tokens.
    """
    left = 0
    right = 0
    n = len(s)

    result = []

    while right < n and left <= right:
        if not isDelimiter(s[right]):
            right += 1

        if left == right and isDelimiter(s[right]):
            if s[right] not in [" ", "\t", "\n"]:
                if isMathOperator(s[right]):
                    result.append("MATH_OPERATOR")
                elif isBoolOperator(s[right]):
                    result.append("BOOL_OPERATOR")
                else:
                    result.append(s[right])
            right += 1
            left += 1

        if (right == n and left != right) or (left != right and isDelimiter(s[right])):
            subs = s[left:right]
            if subs in key_words_dic:
                result.append(key_words_dic[subs])

            elif is_integer(subs):
                result.append("INTEGER")
            elif is_float(subs):
                result.append("FLOAT")
            elif is_valid_identifier(subs) and not isDelimiter(s[right - 1]):
                result.append("ID")
            else:
                print("\nThe analyzed tokens are: \n")
                print(result)
                print("\n")
                lexical_error()
                print("\n")
                return
            left = right

    print("\n\nThe tokens are: \n")
    print(result)
    print("\n")
    return result


######################################################################################################
"""
Syntax analyzer 
"""


def switchstmt():
    global s
    s.pop(0)
    if not s or s[0] != "(":
        error()
        return
    s.pop(0)

    if not s or s[0] != "ID":
        error()
        return
    s.pop(0)

    if not s or s[0] != ")":
        error()
        return
    s.pop(0)

    if not s or s[0] != "{":
        error()
        return
    s.pop(0)

    casestmt()
    if not s or s[0] != "}":
        error()
        return
    s.pop(0)


def casestmt():
    global s
    if not s:
        error()
        return
    if s[0] == "CASE_CODE":
        s.pop(0)

    factor()
    if not s:
        return
    if s[0] == ":":
        s.pop(0)
    if not s:
        return
    block()


def foreachstmt():
    global s
    s.pop(0)

    if not s or s[0] != "(":
        error()
        return
    s.pop(0)

    if not s or s[0] != "ID":
        error()
        return
    s.pop(0)
    if not s:
        return

    if s[0] != ";":
        error()
        return
    s.pop(0)
    if not s:
        return

    if s[0] != "ID":
        error()
        return
    s.pop(0)
    if not s:
        return

    if s[0] != ")":
        error()
        return
    s.pop(0)
    block()


def block():
    """
         <block> --> "{" {<statement>} "}" “;”
    """
    global s
    if not s:
        error()
        return
    if len(s) < 3:
        error()
        return

    if s == "{};":
        s = ""
        return

    if s[0] != "{":
        error()
        s = ""
        return

    s.pop(0)
    while s and s[0] != "}":
        statement()

    if not s:
        error()
        return

    if len(s) == 1:
        error()
        s = ""
        return

    if s[0] == "}" and s[1] == ";":
        s.pop(0)
        s.pop(0)
        return
    else:
        error()
        s = ""
        return


# <assign> --> id = < term >
# <term> --> <factor> { (+/-/*|/|%) <factor> }
# <factor> --> identifier | int | float
def factor():
    global s
    if not s:
        error()
        return
    if s[0] in ["ID", "INTEGER", "FLOAT"]:
        s.pop(0)
        return
    else:
        error()
        return


def term():
    global s
    factor()
    if s and s[0] != "MATH_OPERATOR":
        return
    if len(s) < 3:
        error()
        return
    if not s or s[0] != "MATH_OPERATOR":
        error()
        s = ""
        return
    s.pop(0)
    factor()


def assign():
    global s
    if not s:
        return
    if s[0] not in ["ID"]:
        error()
        s = ""
        return
    s.pop(0)
    if not s:
        return
    if s[0] != "=":
        error()
        s = ""
        return
    s.pop(0)
    if not s:
        return
    term()


def boolstmt():
    global s
    if len(s) < 3:
        error()
        s = ""
        return
    if (
        s[0] in ["ID", "INTEGER", "FLOAT"]
        and s[1] == "BOOL_OPERATOR"
        and s[2] in ["ID", "INTEGER", "FLOAT"]
    ):
        s.pop(0)
        s.pop(0)
        s.pop(0)
        if not s:
            return
        return
    else:
        error()
        return


def whilestmt():
    global s
    s.pop(0)
    if not s:
        error()
        return
    if s[0] != "(":
        error()
        return
    s.pop(0)
    if not s:
        error()
        return
    boolstmt()
    if s[0] != ")":
        error()
        return
    s.pop(0)
    if not s:
        error()
        return
    block()


def forstmt():
    global s
    s.pop(0)

    if not s or s[0] != "(":
        error()
        return
    s.pop(0)  # (
    if not s or s[0] != "ID":
        error()
        return
    s.pop(0)  # (

    if not s or s[0] != ";":
        error()
        return
    s.pop(0)
    boolstmt()
    if not s or s[0] != ";":
        error()
        return
    s.pop(0)
    assign()
    if not s or s[0] != ")":
        error()
        return
    s.pop(0)  # )
    block()


def ifstmt():
    global s
    if s[0] == "IF_CODE":
        s.pop(0)
        if not s or s[0] != "(":
            error()
            return
        s.pop(0)
        boolstmt()
        if not s or s[0] != ")":
            error()
            return
        s.pop(0)
        block()
        if s:
            if s[0] != "ELSE_CODE":
                return
            if s[0] == "ELSE_CODE":
                s.pop(0)
                block()


def dowhilestmt():
    global s
    if s[0] != "DO_CODE":
        error()
        return
    s.pop(0)
    block()
    if not s or s[0] != "WHILE_CODE":
        error()
        return
    s.pop(0)

    if not s or s[0] != "(":
        error()
        return
    s.pop(0)
    boolstmt()
    if not s or s[0] != ")":
        error()
        return
    s.pop(0)
    return


def returnstmt():
    global s
    if s[0] != "RETURN_CODE":
        error()
        return
    s.pop(0)

    if not s:
        error()
        return
    factor()


def error():
    global s
    global syntax_flag
    syntax_flag = 0
    s = ""
    print("Error Detected!")


def statement():
    # <statement> --> <ifstmt> | <assign>; | <returnstmt>;|<forstmt>|<foreachstmt>|<dowhilestmt>|<whilestmt>|<switchstmt>
    global s
    if not s:
        return
    if s[0] == "IF_CODE":
        ifstmt()
    elif s[0] == "FOR_CODE":
        forstmt()
    elif s[0] == "SWITCH_CODE":
        switchstmt()
    elif s[0] == "FOREACH_CODE":
        foreachstmt()
    elif s[0] == "DO_CODE":
        dowhilestmt()
    elif s[0] == "WHILE_CODE":
        whilestmt()
    elif s[0] == "RETURN_CODE":
        returnstmt()
    else:
        assign()


def syntax_parse():
    program()


def program():
    global s
    if not s:
        return
    if len(s) < 5:  # do not have enough length for a program.
        error()
        return
    firsts = ["VOID_CODE", "MAIN_CODE", "(", ")"]
    for i in range(len(firsts)):
        if s[i] != firsts[i]:
            error()
            return
    s = s[4:]
    block()


######################################################################################################
# Main Program
f = open("program.txt", "r")
s = lexical_parse(f.read())
syntax_flag = 1
syntax_parse()
if syntax_flag:
    print("No Syntax Error Detected.")
