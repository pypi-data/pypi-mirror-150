import os,time,sys

alphs = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def renderText(string, writetime, end="\n"):
        os.system('clear')
        os.system('clear')
        for char in string + end:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(writetime)

def deleteText(wait):
        time.sleep(wait)
        os.system('clear')

def PythonRunner(filename=""):
        """Creates A Python Interpreter"""
        print("User@Desktop $ ", end="")
        for char in f'bash -f python.sh -- {filename}\n':
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.1)
        time.sleep(0)
        exec(open(filename).read())
