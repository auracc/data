from math import e, hypot
from collections import deque

class Graph:
    def get_dest(self,point):
        dest = None
        pd = self.points[point]
        if 'dest' in pd:
            dest = pd['dest']
        return dest

    def generate_nodes(self):
        # ----- Generate the A* node list ----- (todo: add distance)
        adjac_lis = {}
        for line in self.lines:
            ps = line['points']
            # Line name, either using the line's name or generating one if direct connection 
            if 'name' in line:
                line_name = line['name']
            else:
                line_name = '{} - {}'.format(ps[0],ps[-1])

            # Iterate all points in the line
            for i in range(len(ps)):
                p = ps[i]
                p_data = self.points[p]

                dat = []
                if p in adjac_lis:  # check if this point has already been added
                    dat = adjac_lis[p]

                # Dest A
                if i > 0:
                    n_data = self.points[ps[i-1]]
                    d = hypot(p_data['x']-n_data['x'],p_data['z']-n_data['z'])
                    if 'dest_a' in line:
                        dat.append((ps[i-1],d,line['dest_a'],line_name))
                    else:
                        dat.append((ps[i-1],d,self.get_dest(ps[0]),line_name))
                # Dest B
                if i < len(ps) - 1:
                    n_data = self.points[ps[i+1]]
                    d = hypot(p_data['x']-n_data['x'],p_data['z']-n_data['z'])
                    if 'dest_b' in line:
                        dat.append((ps[i+1],d,line['dest_b'],line_name))
                    else:
                        dat.append((ps[i+1],d,self.get_dest(ps[-1]),line_name))

                adjac_lis[p] = dat

        return adjac_lis

    def __init__(self, points,lines):
        self.lines = lines
        self.points = points
        self.adjac_lis = self.generate_nodes()
        
 
    def get_neighbors(self, v, line=None):
        return self.adjac_lis[v]
 
    # This is heuristic function which is having equal values for all nodes
    def h(self, n):
        #return H[n]
        return 1

    def add_to_dest(self,dest,n,stop=False):
        to_append = n
        extra = None
        if n in self.points:
            t = self.points[n]['type']
            if not t == 'crossing':
                to_append = self.points[n]['dest']
                t = self.points[n]['type']
                if stop:
                    if t == 'junctionstop':
                        extra = self.points[n]['dest_stop']
                else:
                    if t == 'stopjunction':
                        extra = self.points[n]['dest_junction']
            else:
                return dest

        if not to_append in dest:
            dest.append(to_append)
        if extra:
            dest.append(extra)
        return dest
 
    def a_star_algorithm(self, start, stop):
        # In this open_lst is a lisy of nodes which have been visited, but who's 
        # neighbours haven't all been always inspected, It starts off with the start 
  #node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always inspected
        open_lst = set([start])
        closed_lst = set([])

        
 
        # poo has present distances from start to all other nodes
        # the default value is +infinity
        poo = {}
        poo[start] = 0
 
        # par contains an adjac mapping of all nodes
        par = {}
        par[start] = (start,None,None)
 
        while len(open_lst) > 0:
            n = None
 
            # it will find a node with the lowest value of f() -
            for v in open_lst:
                if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v;
 
            if n == None:
                print('Path does not exist!')
                return None
 
            # if the current node is the stop
            # then we start again from start
            if n == stop:
                reconst_path = []
                dest = []

                #print(par)
 
                while par[n][0] != n:
                    reconst_path.append(n)
                    n = par[n][0]
 
                reconst_path.append(start)
                reconst_path.reverse()

                # Generating the /dest command 
                last_dest = None
                last_point = None
                last_line = None
                for point in reconst_path:
                    this_line = par[point][2]
                    this_dest = par[point][1]
                    if this_line != last_line and this_line != None and last_point != start:
                        dest = self.add_to_dest(dest,last_point)
                    if this_dest != None:
                        dest = self.add_to_dest(dest,this_dest)

                    last_point = point
                    last_line = this_line
                    last_dest = this_dest
                    
                
                dest = self.add_to_dest(dest,stop,stop=True)

                print('Path found: {}'.format(reconst_path))
                #print(dest)
                print("/dest {}".format(" ".join(dest)))
                return reconst_path,dest

            # for all the neighbors of the current node do
            for (m, weight, dest,line) in self.get_neighbors(n):
                if line == par[n][2] or self.points[n]['type'] != 'stop' or n == start:
                    # if the current node is not presentin both open_lst and closed_lst
                    # add it to open_lst and note n as it's par
                    if m not in open_lst and m not in closed_lst:
                        open_lst.add(m)
                        par[m] = (n,dest,line)
                        poo[m] = poo[n] + weight

                    # otherwise, check if it's quicker to first visit n, then m
                    # and if it is, update par data and poo data
                    # and if the node was in the closed_lst, move it to open_lst
                    else:
                        if poo[m] > poo[n] + weight:
                            par[m] = (n,dest,line)
                            poo[m] = poo[n] + weight

                            if m in closed_lst:
                                closed_lst.remove(m)
                                open_lst.add(m)
            # remove n from the open_lst, and add it to closed_lst
            # because all of its neighbors were inspected
            open_lst.remove(n)
            closed_lst.add(n)
 
        print('Path does not exist!')
        return None,None