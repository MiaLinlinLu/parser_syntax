# grammars:
# <program>    ->  VOID MAIN () <block> ";"
# <block>      ->'{' {<statement>}  <returnstmt> '}'
# <classdef>   ->  Class <ID> '{'{<function>|<statement>} '}'   
# <function>   ->  def <ID> '('  {<assign>|<factor>}  ')' '=>' <Type>  <block>  
# <statement>   --> <staticvar> | <declarevar> |  <assign> |  <classdef> | <function>
# <returntypes>  --> 'Int'|'String'|'VOID'|'Float'|'Bool'|<Class>
# <returnstmt> --> return {<factor>}

# <assign>    --> <ID> = <term> | <boolstmt>
# <term>      --> <factor> { ( '+' | '-' | '*' | '/' | '%') <factor> }
# <factor>    --> identifier | int | float | string| <varDeref>
# <boolstmt>   --> TRUE_CODE | FALSE_CODE | (<term> (">"|"<"|"==") <term>)

# <staticvar>  ->  static <declarevar> 
# <declarevar> ->  <Types> <ID>

# <voidtype>   ->  <VOID> 
# <String>       -->  ''  //using single quotes
# <int>          -->  0| ((1|2|3|4|5|6|7|8|9){0|1|2|3|4|5|6|7|8|9})
# <Float>        --> <int>"."<int>
# <Bool>         --> <boolstmt>
# <varDeref>     --> '*'<ID>

"""
Syntax analyzer 
"""
import lexical_parser as lex

'''
define lists/dics.
'''
type_dic = {}    # {id:type}
static_vars = [] # [id]
class_vars = []  #[class1,class2,...]
class_dic = {}   #{class_name:[[vars_list],[methods_list]]}
function_dic = {} # {function_name:[arg_list]}


def block(return_type=None):
    """
         <block> --> "{" {<statement>} "}" “;”
    """
    vars_list = []
    methods_list = []
    print("Enter <block>\n")
    global s
    if (not s) or (s[0] != "{"):
        error()
        return
    s.pop(0)
    while s and (s[0] not in ["}","RETURN_CODE"]):
        a_list,b_list = statement()
        vars_list += a_list
        methods_list += b_list

    returnstmt(return_type = return_type)

    if len(s)>=2 and s[0]=='}' and s[1]==";":
        s.pop(0)
        s.pop(0)
        print("EXIT <block>\n")
        return vars_list,methods_list
    else:
        error()
        return

# <assign> --> id = < term >
# <term> --> <factor> { (+/-/*|/|%) <factor> }
# <factor> --> identifier | int | float
def factor(return_type=None):
    print("ENTER <factor>\n")
    global s
    if not s:
        error()
        return
    if not return_type:
        print(s[0])
        if s[0] in ["INTEGER", "FLOAT","STRING","BOOL"]:
            print("EXIT <factor>\n")
            s.pop(0)
            return  
        elif s[0]=='ID' and s[1] in type_dic:
            print("EXIT <factor>\n")
            s.pop(0)
            s.pop(0)
            return  
        elif s[0]=='varDeref' and s[2] in type_dic:
            print("EXIT <factor>\n")
            s.pop(0)
            s.pop(0)
            s.pop(0)
            return 
        elif s[0]=='ID' and ('.' in s[0]):
            tempz = s[0].split('.')   
            if len(tempz)==2:
                classname,varmethod = tempz
                if (classname in class_dic) and (varmethod in class_dic[classname][0]+class_dic[classname][1]):
                    s.pop(0)
                    s.pop(0)
                    print("EXIT <factor>\n")
                    return

        error()
        print("wrong type of factor")
        return
    else:
        if s[0]=='ID' and s[1] in type_dic:
            this_type = type_dic[s[1]]
            s.pop(0)
            s.pop(0)
        elif s[0]=="varDeref":
            if s[2] in type_dic:
                this_type = type_dic[s[2]]
                s.pop(0)
                s.pop(0)
                s.pop(0)
            else:
                print("undefined ID name:{}".format(s[2]))
                error()
                return
        elif s[0]=="INTEGER":
            this_type = 'Int'
            s.pop(0)
        elif s[0]=="FLOAT":
            this_type = 'Float'
            s.pop(0)
        elif s[0]=='BOOL':
            this_type = 'Bool'
            s.pop(0)
        elif s[0]=='STRING':
            this_type = 'String'
            s.pop(0)
        else:
            error()
            print("undefined type.")
            return
        if return_type==this_type:
                print("EXIT <factor>\n")
                return
        else:
            print("wrong return type")
            error()
            return


def declarevar():
    '''
    return [new_id list],[new_method list]
    '''
    print("ENTER <declarevar>\n")
    global s
    if not s:
        error()
        return
    # type code
    if s[0] in ['Int','Float','VOID_CODE','String','Bool']:
        new_type = s[0]
        s.pop(0)
    # 
    elif s[0]=='ID' and s[1] in class_vars:
        new_type = s[1]
        s.pop(0)
        s.pop(0)
    else:
        error()
        print('wrong type,type does not exist')
        return
    # id
    if not s or s[0] not in ['ID','varDeref']:
        print("ID required")
        error()
        return
    if s[0]=='varDeref':
        s.pop(0)
    new_id = s[1]
    s.pop(0)
    s.pop(0)
    if new_id in type_dic:
        error()
        print("ID: {} cannot be declared twice!\n".format(new_id))
        return
    type_dic[new_id] = new_type
    print("EXIT <declarevar>\n")
    return [new_id],[]

# term: factor | factor +-*/% factor
def term():
    print("ENTER <term>\n")
    global s
    if not s:
        error()
        print("there should be at least one factor here.")
        return
    factor()
    while s and s[0]=='MATH_OPERATOR':
        s.pop(0)
        factor()
    if not s or s[0] != "MATH_OPERATOR":
        print("EXIT <term>\n")
        return


def assign():
    print("ENTER <assign>\n")
    global s
    if not s:
        return
    print(s[0])
    if s[0]!='ID':
        print("The assign statement should start with an ID.\n")
        print("However,it starts with {}".format(s[0]))
        error()
        return
    this_id = s[1]
    s.pop(0)
    s.pop(0)
    if '.' in this_id:
        tempz = this_id.split('.')   
        if len(tempz)==2:
            classname,varmethod = tempz
            if not ((classname in type_dic) and (type_dic[classname] in class_vars) and (varmethod in class_dic[type_dic[classname]][0]+class_dic[type_dic[classname]][1])):
                error()
                print("wrong id")
                return
            else:
                type_dic[this_id] = 'class_deref'
        else:
            error()
            print("wrong id provided")
            return
    elif this_id not in type_dic:
        error()
        print('ID : {} not defined'.format(this_id))
        return 
    if type_dic[this_id]=='Bool':
        if not s:
            print("Wrong code. Here requires a bool variable or statement")
            error()
            return
        if s[0]!='=':
            print("lacking = for assignment")
            error()
            return
        s.pop(0)
        boolstmt()
        print("EXIT <assign>\n")
        return [this_id],[]

    if not s or s[0] != "=":
        error()
        print("= is required for assignment.")
        return
    s.pop(0)
    if not s:
        error()
        return
    term()
    print("EXIT <assign>\n")
    return [this_id],[]


def boolstmt():
    print("ENTER <boolstmt>\n")
    global s
    print(s[0])
    if not s:
        error()
        s = ""
        print("there is no bool statement")
        return
    if s[0] in ['TRUE_CODE','FALSE_CODE']:
        print('EXIT <boolstmt>\n')
        s.pop(0)
        return
    term()
    if not s or s[0] != "BOOL_OPERATOR":
        print("need a bool operator here!\n")
        error()
        return
    s.pop(0)
    term()  
    print("EXIT <boolstmt>\n")
    return  


def returnstmt(return_type=None):
    print("ENTER <returnstmt>\n")
    global s
    if (not s) or (s[0]!='RETURN_CODE'):
        print('LACK return statement')
        error()
        return  
    s.pop(0)  
    if not return_type:
        print('EXIT <returnstmt>\n')
        return
    # do not need a return value
    if return_type=='VOID_CODE':
        print('EXIT <returnstmt>\n')
        return 
    # need a return value
    if not s:
        error()
        return
    factor(return_type=return_type)
    print("EXIT <returnstmt>\n")
    return


def error():
    global s
    global syntax_flag
    syntax_flag = 0
    s = ""
    print("Error Detected!")

# <function>   ->  def <ID> '('  {<assign>}  ')' '=>' <Type> <block>   # type(<Type>)==type(<factor>)
def function():
    print("ENTER <function>\n")
    fun_args = []
    global s
    if not s or s[0] != "DEF_CODE":
        error()
        print("'def' is required.")
        return
    s.pop(0)
    if s and s[0]=='static':
        s.pop(0)
    if not s or s[0] != "ID":
        if s:
            print("Function name should be an ID, should not be : {}".format(s[0]))
        error()
        return
    print(s[0])
    s.pop(0)
    function_name = s[0]
    if s[0] in type_dic:
        print("The ID: {} has been declared before.".format(s[0]))
        error()
        return
    s.pop(0)
    if not s or s[0] != '(':
        error()
        print("lacking () for declaring arguments for the function. ")
        return
    s.pop(0)
    if not s:
        print("( is required for the function arguments.")
        error()
        return
    while s and s[0]!=')':
        a_list,_ = assign()
        fun_args += a_list
    if not s or s[0]!=')':
        print(") is required for the function arguments.")       
        error()
        return 
    s.pop(0)   

    if not s or s[0] != "=>":
        print("=> is required for the function.")              
        error()
        return
    s.pop(0)
    if not s:
        print("A return type is required for the function. Choose from Int,Float,String,VOID")              
        error()
        return        
    elif s[0] in ['Int','Float','String','VOID_CODE']:
        return_type = s[0]
        s.pop(0)
    elif s[0]=='ID' and (s[1] in class_vars):
        return_type = s[1]
        s.pop(0)
        s.pop(0)
    else:
        print("wrong type of required Return value")              
        error()
        return          
    block(return_type=return_type)   
    print('EXIT <function>\n')
    function_dic[function_name] = fun_args
    return [],[function_name]

# <staticvar>  ->  static <declarevar> 

def staticvar():
    print("ENTER <staticvar>\n")
    if not s or s[0] not in ['Int','Float','VOID_CODE','String']:
        error()
        return
    print(s[0])
    new_type = s[0]
    s.pop(0)
    if not s or s[0]!='ID':
        error()
        return
    new_id = s[1]
    s.pop(0)
    s.pop(0)
    if new_id in type_dic:
        error()
        print("ID cannot be declared twice!\n")
        return
    type_dic[new_id] = new_type
    static_vars.append(new_id)
    print("EXIT <staticvar>\n")
    return [new_id],[]
    

def statement():
    # <statement> --> <assign>; | <returnstmt>;|<forstmt>|<foreachstmt>|<dowhilestmt>|<whilestmt>|<switchstmt>
    global s
    print("ENTER <statement>\n")
    if not s:
        print("EXIT <statement>\n")
        return
    print(s[0])
    if s[0]=='static':
        s.pop(0)
        var_list,method_list = staticvar()
        print("EXIT <statement>\n")
        return var_list,method_list
    elif s[0] in ['Int','String','Float','Bool'] or (s[0]=='ID' and (s[1] in class_vars)):
        var_list,method_list = declarevar()
        print("EXIT <statement>\n")
        return var_list,method_list
    elif s[0]=='CLASS_CODE':
        var_list,method_list =classdef()
        print("EXIT <statement>\n")
        return var_list,method_list
    elif s[0]=='DEF_CODE':
        var_list,method_list = function()
        print("EXIT <statement>\n")  
        return var_list,method_list
    else:
        assign()
        print("EXIT <statement>\n")
        return [],[]


def syntax_parse():
    program()


def program():
    print("Enter <program>\n")
    global s
    if not s:
        print("Exit <program>\n")
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
    block(return_type=None)
    print("Exit <program>\n")

# <classdef>   ->  Class <ID> '{' {assign} {<function>} '}'  
def classdef():
    global s
    if not s or s[0]!='CLASS_CODE':
        error()
        return 
    s.pop(0)
    if not s or s[0]!='ID':
        error()
        return 
    new_class = s[1]
    if s[1] in type_dic:
        print('Class name is already taken.')
        error()
        return
    class_vars.append(new_class)
    s.pop(0)   
    s.pop(0)
    if not s or s[0]!='{':
        error()
        print("Class need a <block>")
        return 
    vars_list, methods_list = block()  
    print("EXIT <classdef>\n")
    class_dic[new_class]=[vars_list,methods_list]
    return vars_list,methods_list

######################################################################################################
# Main Program
f = open("program.txt", "r")
s = lex.lexical_parse(f.read())
if s:
    syntax_flag = 1
    syntax_parse()
    print('\n\n----------all variables types are:---------------')
    print(type_dic)
    print('\n\n----------all Class variables are:---------------')
    print(class_vars)
    print('\n\n----------all defined Class names and their [variables] and [methods] are:---------------')
    print(class_dic)
    print('\n\n----------all Function arguments are:---------------')
    print(function_dic)    
    print('\n\n----------all Static vars and functions are:---------------')
    print(static_vars)      
    if syntax_flag:
        print("No Syntax Error Detected.")