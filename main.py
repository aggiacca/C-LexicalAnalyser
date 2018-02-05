import re

KEYWORDS = ['else', 'if', 'int', 'return', 'void', 'while']


class token():
    def __init__(self,nm,class_nm,ind):
        self.name = nm
        self.class_name = class_nm
        self.index = ind

def stripComments(str):
    comment_regex = re.compile(r"/\*.*?\*/")
    results = comment_regex.findall(str)

    new_str = str
    for match in results:
        new_str = new_str.replace(match, "")
    return new_str

def generateSymbolTables(code_str):

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
        token = token_pattern_re.match(code_str, pos)
        if not token:
            break
        pos = token.end()
        token_name = token.lastgroup
        token_value = token.group(token_name)

        print("token:{}, {} ".format(token_name, token_value))

        if token_value in KEYWORDS:
            if token_value not in keywords:
                keywords.push(token_value)
        elif token_name is "identifier":
            if token_value not in identifiers:
                identifiers.push(token_value)
        elif token_name is "integer" or token_name is "float":
            if token_value not in numbers:
                numbers.push(token_value)



    if pos != len(code_str):
        raise Exception('tokenizer stopped at pos %r of %r' % (
            pos, len(code_str)))


if __name__ == '__main__':
    # user input file
    #inputFile = input("Enter File name: ")
    #rawFile = open(inputFile,'r')

    rawFile = open('loudenCode.txt', 'r')

    codeWithComments = rawFile.read()
    print(codeWithComments)

    code_wo_comments = stripComments(codeWithComments)
    print(code_wo_comments)

    generateSymbolTables(code_wo_comments)

