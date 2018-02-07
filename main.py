import re



class Token:
    def __init__(self, nm, class_nm, ind):
        self.name = nm
        self.class_name = class_nm
        self.index = ind


class Number:
    def __init__(self, val, num_tp):
        self.value = val
        self.num_type = num_tp


def printTable(list):
    for index, item in enumerate(list):
        print(item + ' | ' + str(index))


def printTables(keywords, identifiers, numbers, tokens):
    print("Keyword Table:")
    print("-----------------------")
    printTable(keywords)

    print("Identifiers Table:")
    print("-----------------------")
    printTable(identifiers)

    print("Numbers Table:")
    print("-----------------------")
    for index, item in enumerate(numbers):
        print(item.value + ' | ' + str(index) + ' | ' + item.num_type)

    print("Token Table:")
    print("-----------------------")
    for token in tokens:
        print(token.name + ' | ' + token.class_name + ' | ' + str(token.index))

def stripComments(str):
    comment_regex = re.compile(r"/\*.*?\*/")
    results = comment_regex.findall(str)

    new_str = str
    for match in results:
        new_str = new_str.replace(match, "")
    return new_str

def generateSymbolTables(code_str):

    KEYWORDS = ['else', 'if', 'int', 'return', 'void', 'while']

    keywords = []
    identifiers = []
    numbers = []
    tokens = []

    token_patterns = r"""
    (?P<identifier>[a-zA-Z_][a-zA-Z_]*)
    |(?P<integer>[0-9]+)
    |(?P<float>[0-9].[0-9]+)
    |(?P<dot>\.)
    |(?P<open_variable>[$][{])
    |(?P<open_curly>[{])
    |(?P<close_curly>[}])
    |(?P<newline>\n)
    |(?P<whitespace>\s+)
    |(?P<specialchar>[\+|\-|\*|\/|\<|\>|\!|\=|\;|\,|\(|\)|\[|\]])
    """
    token_pattern_re = re.compile(token_patterns, re.VERBOSE)

    pos = 0
    while True:
        # get next token
        token = token_pattern_re.match(code_str, pos)
        if not token:
            break
        pos = token.end()
        token_name = token.lastgroup
        token_value = token.group(token_name)

        # print for testing
        # print("token:{}, {} ".format(token_name, token_value))

        # add token to tables
        if token_name == 'identifier':
            if token_value in KEYWORDS:
                if token_value not in keywords:
                    keywords.append(token_value)
                    # add to token table as well
                    tokens.append(Token(token_value, token_name, keywords.index(token_value)))
            else:
                if token_value not in identifiers:
                    identifiers.append(token_value)
                    tokens.append(Token(token_value, token_name, identifiers.index(token_value)))
        elif token_name == 'integer' or token_name == 'float':
            if token_value not in numbers:
                num = Number(token_value, token_name)
                numbers.append(num)
                tokens.append(Token(token_value, token_name, numbers.index(num)))
        else:
            tokens.append(Token(token_value, token_name, -1))

    # Error checking
    if pos != len(code_str):
        raise Exception('Token Parser stopped at position {} of {} input code. Please double token at position is in correct format'.format(pos, len(code_str)))

    # print tables
    printTables(keywords, identifiers, numbers, tokens)

if __name__ == '__main__':
    # user input file
    inputFile = input("Enter File name: ")
    rawFile = open(inputFile, 'r')
    #rawFile = open('loudenCode.txt', 'r')

    codeWithComments = rawFile.read()
    code_wo_comments = stripComments(codeWithComments)
    print(code_wo_comments)

    generateSymbolTables(code_wo_comments)

