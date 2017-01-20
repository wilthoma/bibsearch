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

parser.add_argument('-f', metavar='F', type=str, nargs='+', default='.',
                    help='search in specific file(s) or folder(s)')


args = parser.parse_args()
#print args.strings
#print args.n
#print args.f


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
        print( "*********** " + f )
        for m in matches:
            print(m +"\n")




#mypath = os.path.curdir

def parsedir(dir):
    for file in os.listdir(dir):
        ff = os.path.join(dir, file)
        if os.path.isdir(ff) and not args.n:
            parsedir(ff)
        if file.endswith(".tex"):
            parseFile(ff, args.strings)



for path in args.f:
    if os.path.isdir(path):
        parsedir(path)
    elif os.path.isfile(path):
        parseFile(path)
    else:
        print "Not found: "+path



