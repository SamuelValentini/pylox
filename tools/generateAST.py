exprAST = (
    "Expr",
    {
        "Binary": ("left", "operator", "right"),
        "Call": ("callee", "paren", "arguments"),
        "Get": ("obj", "name"),
        "Grouping": ("expr",),
        "Literal": ("value",),
        "Logical": ("left", "operator", "right"),
        "Set": ("obj", "name", "value"),
        "Super": ("keyword", "method"),
        "This": ("keyword",),
        "Unary": ("operator", "right"),
        "Variable": ("name",),
        "Assignment": ("name", "value"),
    },
)

stmtAST = (
    "Stmt",
    {
        "Expression": ("expression",),
        "Function": ("name", "params", "body"),
        "Print": ("expression",),
        "Return": ("keyword", "value"),
        "Var": (
            "name",
            "initializer",
        ),
        "While": ("condition", "body"),
        "Block": ("statements",),
        "Class": ("name", "superclass", "methods"),
        "If": ("condition", "thenBranch", "elseBranch"),
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


def printVisitor(subclasses, baseClassName, baseClass):
    visitor = f"../pylox/{baseClass}Visitor.py"
    visitor = open(visitor, "w")
    printImport(visitor)
    visitor.write(f"class {baseClass}Visitor(ABC):\n")
    for subcl in subclasses:
        visitor.write("    @abstractmethod\n")
        visitor.write(
            f"    def visit{subcl}{baseClassName}(self, {baseClass.lower()}):\n"
        )
        visitor.write("        pass\n\n")


def createAST(ast, outFile):
    outPath = f"../pylox/{outFile}.py"
    outFile = open(outPath, "w")
    baseClass = ast[0]
    subclasses = ast[1]

    printImport(outFile)
    printBase(baseClass, outFile)
    printSubclasses(subclasses, baseClass, outFile)
    outFile.close()

    printVisitor(subclasses, baseClass, baseClass)


createAST(exprAST, "Expr")
createAST(stmtAST, "Stmt")
