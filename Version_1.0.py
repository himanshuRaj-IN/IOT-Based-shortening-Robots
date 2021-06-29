"""
Author : Himanshu Raj
E-mail : himanshuraj9194@gmail.com

"""
#-------------------------------------------------------------------------------------
from time import sleep
from collections import defaultdict
from heapq import *
#-------------------------------------------------------------------------------------
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1

# Shortest Path Algorithm

# Nodes Data ( Weighted Node Graph
edges = [
#       {{Node_1 } ,{Node_2},{Distance between Them}}
        ("S", "1", 10),
        ("1", "2", 10),
        ("1", "7", 20),
        ("2", "5", 5),
        ("2", "3", 5),
        ("3", "4", 12),
        ("4", "E", 5),
        ("5", "6", 12),
        ("6", "7", 8),
        ("6", "4", 10),
        # ("F", "G", 11)
                        ]


def dijkstra(edges, f, t):
    g = defaultdict(set)
    for l, r, c in edges:
        g[l].add((c, r))
        g[r].add((c, l))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))

    return float("inf"), None

make_path = lambda tup: (*make_path(tup[1]), tup[0]) if tup else ()
out = dijkstra(edges, "S","5")
path = make_path(out[1])
print(path)
print(listToString(path))
print(out)


