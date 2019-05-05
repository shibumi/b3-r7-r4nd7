#!/usr/bin/env python3
#
# Implementation for the get-in-IT and bertrand cooding challenge on:
# https://www.get-in-it.de/coding-challenge#mitmachen
#
# Author: Christian Rebischke - <christian.rebischke@tu-clausthal.de>
# Date: 2019-05-04
#
# Note: I would have preferred to do this in Golang. It would be a lot faster with Golang.
# I thought about using C++, but the hassle with loading and working with json stopped me doing so.
# This approach is now much shorter and better understandable.

from dijkstar import Graph, find_path  # for actual shortest path calculation
import json  # for reading the json file
import networkx  # for drawing nice graphs as output
import matplotlib.pyplot  # for converting the graph into PDF
import argparse  # for parsing arguments
import sys  # for counting arguments


class Challenge:
    # These are our source/target planets as constants. Yeah, I know.. they are not really constant.. python.. sigh
    EARTH = 18
    BERTRAND = 246

    def __init__(self, galaxy_file="generatedGraph.json"):
        # Open generatedGraph.json as `galaxy` and load all JSON data
        with open(galaxy_file) as galaxy:
            self.galaxy_data = json.load(galaxy)
            # Make sure to close the file handle
            galaxy.close()

        # Initialize the actual graph
        self.graph = Graph()
        # Iterate over all edges
        for edge in self.galaxy_data['edges']:
            # The graph is undirected, so we add source/target and target/source couples to our graph as edges
            self.graph.add_edge(edge['source'], edge['target'], {'cost': edge['cost']})
            self.graph.add_edge(edge['target'], edge['source'], {'cost': edge['cost']})

        # This cost function will just return the cost itself for every node
        self.cost_func = lambda u, v, e, prev_e: e['cost']

    # This method calculates the shortest path. Time complexity is O(len(nodes)^2 in the worst case.
    # In the best case we can achieve a time complexity of O(len(nodes) log len(nodes) + len(edges)).
    def calculate_shortest_path(self):
        # Do the actual calculation. I use the dijkstar python module here, because of a few reasons:
        # 1. Technical debt: I am not a mathematician, therefore it cost me time to implement a fully working dijkstra
        #    single-source shortest-path algorithm by my self. To reduce the cost, I use an implementation by an actual
        #    mathematician. I did code a dijkstra algorithm in C++ during my studies,
        #    but why investing unnecessary time?
        #    In the end it's my time that will be wasted or the time/money of my future employee ;)
        # 2. Complexity: I am not a mathematician, so I will let others do the work in implementing an error-free
        #    dijkstra algorithm
        # 3. Open Source: I think it's better to use existing solutions, and provide patches for these
        #    solutions if they are erroneous. With this workflow we can focus on the actual work and save time/money.
        # 4. I am mostly interested in DevOps and Site-Reliability Engineering.
        #    So I went with the shortest solution as possible with the best effect. This way I can reduce toil.
        path = find_path(self.graph, self.EARTH, self.BERTRAND, cost_func=self.cost_func)
        return path

    # This draws the shortest path in a PDF file
    def draw_shortest_path(self):
        # here we generate a complete graph and calculate the shortest path
        complete_graph = networkx.Graph()
        for i in range(0, 999):
            complete_graph.add_node(i)
        for edge in self.galaxy_data['edges']:
            complete_graph.add_edge(edge['source'], edge['target'])
        path = self.calculate_shortest_path()
        edgelist = []
        # We need to generate an edge list of our shortest path
        # path[0] consist of a list of all our nodes in our shortest path
        for i in range(0, len(path[0])-1):
            edgelist.append((path[0][i], path[0][i+1]))
        # Feel free to increase the figsize if you need more details in our graphic
        # but make sure to stay under a size of 2^16 x 2^16
        matplotlib.pyplot.figure(figsize=(100, 100))
        # Set position layout for our graph. We have a circular layout, for a nice circle structure
        pos = networkx.circular_layout(complete_graph)
        # we draw the actual graph with all labels
        networkx.draw(complete_graph, pos, font_size=8, with_labels=True)
        # And now we color our shortest path (nodes + edges) red and increase the size of them
        networkx.draw_networkx_nodes(complete_graph, pos, nodelist=path[0], node_color='r', node_size=500)
        networkx.draw_networkx_edges(complete_graph, pos, edgelist=edgelist, edge_color='r', width=10)
        # Ok let's plot the graphic
        matplotlib.pyplot.savefig("challenge.pdf")

    # Pretty print method.. just outputs some statistics in nice format
    def pretty_print(self):
        print()
        print("------ Statistics ------")
        path = self.calculate_shortest_path()
        print("Shortest path: ", end='')
        for i in range(0, len(path[0])):
            print(path[0][i], end='')
            if i != len(path[0])-1:
                print(" <--> ", end='')
        print()
        print("Edge costs   : ", end='')
        print(path[2])
        print("Total cost   : ", path[3])
        print("------------------------")
        print()


# This is the entrypoint for our program
if __name__ == '__main__':
    challenge = Challenge()
    # we use the argparser to parse arguments
    parser = argparse.ArgumentParser(description='Find the shortest path for the get-in-IT/bertrand challenge')
    parser.add_argument('--statistics', '-s', help='Print statistics in ASCII', action='store_true')
    parser.add_argument('--graphic', '-g', help='Generate statistics as PDF format', action='store_true')
    args = parser.parse_args()
    # If we have less than two arguments, we print the help output
    if len(sys.argv) < 2:
        parser.print_help()
    if args.statistics:
        challenge.pretty_print()
    if args.graphic:
        challenge.draw_shortest_path()
