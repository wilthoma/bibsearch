#!/usr/bin/env python
import argparse
import os 

parser = argparse.ArgumentParser(description='Searches for a bib entry in tex files.')

parser.add_argument('strings', metavar='S', type=str, nargs='+',
                    help='strings to be included in the entry')
#parser.add_argument('-r', dest='accumulate', action='store_const',
#                    const=1, default=0,
#                    help='recurse subfolders (default: only current folder)')
parser.add_argument('-n', action='store_true',
                    help='do not recurse subfolders (default: recurse)')

parser.add_argument('-f', metavar='F', type=file,
                    help='search in specific file')


args = parser.parse_args()
#print args.strings
#print args.n
#print args.f

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parseFile(f, strings):
    #print("Processing: " + f)
    bibitems=[]
    curitem=""
    inblock=False
    initem=False
    with open(f, 'r') as fi:
        for line in fi:
            l = line.lstrip()
            if l.startswith('%'):
                pass
            elif l.startswith('\\begin{thebibliography}'):
                inblock=True
                curitem=""
                initem=False
            elif l.startswith('\\end{thebibliography}'):
                inblock=False
                if initem:
                    bibitems.append(curitem)
                initem=False
            elif inblock:
                if l.startswith('\\bibitem'):
                    if initem:
                        bibitems.append(curitem)
                    initem=True 
                    curitem=""
                if initem and not l.isspace():
                    curitem = curitem + line # + '\n'

    matches = []
    for b in bibitems:
        if all(s.lower() in b.lower() for s in strings):
            matches.append(b.strip())
    matches = list(set(matches))
    if  matches:
        print( "*********** Matches found in: " + f )
        for m in matches:
            print(m +"\n")




mypath = os.path.curdir

def parsedir(dir):
    for file in os.listdir(dir):
        ff = os.path.join(dir, file)
        if os.path.isdir(ff) and not args.n:
            parsedir(ff)
        if file.endswith(".tex"):
            parseFile(ff, args.strings)
        
parsedir(mypath)



