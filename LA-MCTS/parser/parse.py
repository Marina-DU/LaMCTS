from antlr4 import *
from parser.grammar.IGLexer import IGLexer
from parser.grammar.IGParser import IGParser

from parser.visitor import Visitor
import time

class Parser:

    def __init__(self, path:str, filename:str, verbose:int) -> None:
        self.inputFileName = path + filename +".smb"
        self.visitor = Visitor()
        self.verbose = verbose

    def parse(self) -> Visitor:
        start_time = time.time()

        fs = FileStream(self.inputFileName)
        print(fs)
        lexer = IGLexer(fs)
        stream = CommonTokenStream(lexer)
        parser = IGParser(stream)
        progContext = parser.prog()

        syntaxErrorsCount = parser.getNumberOfSyntaxErrors()
        if syntaxErrorsCount > 0:
            raise Exception(" *** Failure -> " , syntaxErrorsCount , " syntax errors *** ")
        else:
            visitor = Visitor()
            visitor.visit(progContext)
            semanticErrorsCount = visitor.getErrorCounter()
            if semanticErrorsCount > 0:
                raise Exception(" *** Failure -> " , semanticErrorsCount , " semantic errors *** ")

        if self.verbose == 1:
            elapsed_time = time.time() - start_time
            print("\nTime for parsing SMB file " , elapsed_time , "ms")

        return visitor