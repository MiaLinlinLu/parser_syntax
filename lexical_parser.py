

# define DELIMITERa
def isDelimiter(ch):
    this_s = " +-=*/><(:){;}=%'"
    if ch in list(this_s) + ["\t", "\n"]:
        return True
    return False

def isString(ch):
    if ch[0]=="'" and ch[-1]=="'":
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


# INTEGER
def is_integer(s):
    if not s:
        return False
    this_s1 = "123456789"
    this_s = "0123456789"
    if s == "0":
        return True
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
    "Class":"CLASS_CODE",
    "def":"DEF_CODE",
    "true":"TRUE_CODE",
    "false":"FALSE_CODE"
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
                    if result and result[-1]=='=':
                        result[-1] = '=>'
                    else:
                        result.append("BOOL_OPERATOR")
                else:
                    if s[right]=='=':
                        if result and result[-1]=='=':
                            result[-1]= 'BOOL_OPERATOR'
                        else:
                            result.append('=')
                    elif s[right]=="'":
                        right += 1
                        left += 1
                        while right<n and s[right]!="'":
                            right += 1
                            left += 1
                        if right==n:
                            lexical_error()
                            print("Need an ' for the string.")
                            return 
                        result.append('STRING')
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
                if left>0 and s[left-1]=='*':
                    result[-1]= "varDeref"
                    result.append('ID')
                    result.append(subs)
                else:
                    if subs in ['Int','Float','String','VOID','Bool','static']:
                        result.append(subs)
                    else:
                        result.append("ID")
                        result.append(subs)
            else:
                print("\nThe analyzed tokens are: \n")
                print(result)
                print("\n")
                print("{} could not be identified\n".format(subs))
                lexical_error()
                return 0
            left = right

    print("\n\nThe tokens are: \n")
    print(result)
    print("\n")
    return result