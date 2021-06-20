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

def main(argv):
    start = None
    end =  None
    
    
    try:
      opts, args = getopt.getopt(argv,"hf:t:l",["help","from=","to=","listpoints"])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print ('test.py --from <point> -to <point>')
            print ('test.py --listpoints')
            sys.exit()
        elif opt in ("-f", "--from"):
            start = arg
        elif opt in ("-t", "--to"):
            end = arg
        elif opt in ("-l","--listpoints"):
            for p in points.keys():
                print(p)

    if start != None and end != None:
        graph1 = Graph(points,lines)
        graph1.a_star_algorithm(start,end)
    else:
        print ('prototype.py --help')

#if __name__ == "__main__":
#   main(sys.argv[1:])

graph1 = Graph(points,lines)

#graph1.a_star_algorithm('little_leningrad','little_ukraine')
#graph1.a_star_algorithm('csa_main','little_ukraine')
#graph1.a_star_algorithm('pripyat','mount_september')


calculated = {}

for p1 in points:
    for p2 in points:
        if points[p1]['type'] != 'crossing' and points[p2]['type'] != 'crossing':
            path,dest = graph1.a_star_algorithm(p1,p2)
            if path != None and dest != None:
                calculated["{} - {}".format(p1,p2)] = "/dest {}".format(" ".join(dest))

with open('computed.json','w') as f:
    f.write(json.dumps(calculated))
