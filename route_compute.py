from graph import Graph
import json
import sys, getopt

def load_data():
    # ----- Load the rail data -----
    points = {}
    lines = []
    with open('points.json','r') as f:
        points = json.loads(f.read())
    with open('lines.json','r') as f:
        lines = json.loads(f.read())

    return points,lines

points,lines = load_data()

graph1 = Graph(points,lines)
calculated = {}

for p1 in points:
    for p2 in points:
        if points[p1]['type'] != 'crossing' and points[p2]['type'] != 'crossing':
            path,dest = graph1.a_star_algorithm(p1,p2)
            if path != None and dest != None:
                calculated["{} - {}".format(p1,p2)] = "/dest {}".format(" ".join(dest))

with open('computed.json','w') as f:
    f.write(json.dumps(calculated))
