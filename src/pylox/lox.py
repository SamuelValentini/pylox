import sys

hadError = False

def main():
    if len(sys.argv) > 2:
        print("Usage: pylox [script]")
        quit()
    elif len(sys.argv) == 2:
        print(sys.argv[1])
        runFile(sys.argv[1])
    else:
        runPrompt()

def runFile(path):
    with open(path) as f:
        program = f.readlines()

    run(program)

    if(hadError):
        quit()

def runPrompt():
    while(True):
        line = input("> ")
        if line == "":
            quit()
        run(line)
        hadError = False

def run(source):
    scanner = Scanner(source)
    token = scanner.scanTokens()

def error(line, message):
    report(line, "", message)

def report(line, where, message):
    print(f"line: {line}] Error {where}: {message}")
    hadError = True


if __name__ == "__main__":
    main()
