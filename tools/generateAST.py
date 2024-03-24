from re import sub
import sys

exprAST = (
    "Expr",
    {
        "Binary": ("left", "operator", "right"),
        "Grouping": ("expr",),
        "Literal": ("value",),
        "Unary": ("operator", "right"),
    },
)


def printImport(outFile):
    outFile.write("from abc import ABC\n")
    outFile.write("from abc import abstractmethod\n\n")


def printBase(baseClassName, outFile):
    outFile.write(f"class {baseClassName}:\n")
    outFile.write(f"    pass\n\n\n")


def printSubclasses(subclasses, baseClassName, outFile):
    for subcl in subclasses:
        outFile.write(f"class {subcl}({baseClassName}):\n\n")
        outFile.write(f"    def __init__(self, {', '.join(subclasses[subcl])}):\n")
        for field in subclasses[subcl]:
            outFile.write(f"        self.{field} = {field}\n")

        outFile.write("\n")
        outFile.write("    def accept(self,visitor):\n")
        outFile.write(f"        return visitor.visit{subcl}{baseClassName}(self)\n")
        outFile.write(f"\n\n")


def printVisitor(subclasses, baseClassName):
    visitor = open("../pylox/visitor.py", "w")
    printImport(visitor)
    visitor.write("class Visitor(ABC):\n")
    for subcl in subclasses:
        visitor.write("    @abstractmethod\n")
        visitor.write(f"    def visit{subcl}{baseClassName}(self, expression):\n")
        visitor.write("        pass\n\n")


def createAST(ast, outFile):
    outFile = open(outFile, "w")
    baseClass = ast[0]
    subclasses = ast[1]

    printImport(outFile)
    printBase(baseClass, outFile)
    printSubclasses(subclasses, baseClass, outFile)
    outFile.close()

    printVisitor(subclasses, baseClass)


createAST(exprAST, "../pylox/Expr.py")
