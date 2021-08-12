########################################
#             Ryan Oswalt              #
#               8/5/21                 #
#         written in Python3           #
#       tested in Ubuntu 20.04         #
########################################

import fileinput
from pathlib import Path
import sys

# create the edges file if there isn't one; this file contains the records for the flights
Path('edges.txt').touch(exist_ok=True)

def edgeCommand(src, dest, dist, time):
    print("EDGE %s,%s,%s,%s" % (src, dest, dist, time))

def pathCommand(cost, src, dest):
    dests = ""
    for city in dest:
        dests += "," + city
    print("PATH %.2f,%s%s" % (cost, src, dests))

def resultCommand(src, dest):
    print("QUERY %s,%s" % (src, dest))

def malformedCommand(com, args):
    print("MALFORMED %s,%s" % (com, args), file=sys.stderr)

def getPathCost(path):
    return path[0]

def search(src, dest):
    edges_file = open('edges.txt', 'r')
    paths = []

    # check every entry in the records and use backtracking to find every possible path
    for edge_line in edges_file:
        edge = edge_line.strip()
        item = edge.split(',')
        cost = round((float(item[2]) * 15) + (float(item[3]) * 30), 2)
        if item[1] == dest and item[0] == src:
            paths.append([cost, src, [dest]])
        elif item[0] == src:
            result = search(item[1], dest)
            for path in result:
                path_cost = round((path[0] + cost), 2)
                dests = [item[1]]
                for city in path[2]:
                    dests.append(city)
                paths.append([path_cost, src, dests])

    edges_file.close()

    paths.sort(key=getPathCost)
    return paths

def addCommand(src, dest, dist, time):
    new_text = ""
    input_string = "%s,%s,%s,%s" % (src, dest, dist, time)
    update = False
    edges_old = open('edges.txt', 'r')

    # this searches the records file to see if the entry already exists and rewrites the line if it does
    # the file contents are copied and the entry is replaced or appended and then the file is overwritten
    for edge_line in edges_old:
        edge = edge_line.strip()
        new_line = edge
        item = edge.split(',')
        if item[0] == src and item[1] == dest:
            new_line = input_string
            update = True
        new_text += new_line + "\n"
    
    if not update:
        new_text += input_string + "\n"

    edges_old.close()

    edges_new = open('edges.txt', 'w')
    edges_new.write(new_text)
    edges_new.close()

    edgeCommand(src, dest, dist, time)

def queryCommand(src, dest):
    paths = search(src, dest)
    if len(paths) == 0:
        malformedCommand("QUERY", "%s,%s" % (src, dest))
        return

    resultCommand(src, dest)

    for path in paths:
        pathCommand(path[0], path[1], path[2])

for line in fileinput.input():
    # read each line of input and parse the arguments
    line = line.strip()
    parsed = line.split(' ', 1)
    command = parsed[0]
    args = parsed[1].split(',')
    
    invalid = False
    for x in args:
        if x == "":
            invalid = True

    # test that the arguments are valid and run either the ADD or QUERY command
    if (not invalid) and command == "ADD":
        if len(args) == 4:
            src = args[0]
            dest = args[1]
            dist = args[2]
            time = args[3]
            try:
                float(dist)
                float(time)
            except:
                invalid = True
            if not invalid:
                addCommand(src, dest, dist, time)
        else:
            invalid = True
    elif (not invalid) and command == "QUERY":
        if len(args) == 2:
            src = args[0]
            dest = args[1]
            queryCommand(src, dest)
        else:
            invalid = True
    else:
        invalid = True
    
    # each invalid case sets the invalid flag to True, and this checks the flag to avoid calling the function at every instance
    if invalid:
        malformedCommand(command, parsed[1])