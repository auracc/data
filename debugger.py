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
        print ('debugger.py --help')

if __name__ == "__main__":
   main(sys.argv[1:])