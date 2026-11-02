"""
Question 2: Graph - University Course Prerequisite System
==========================================================
A command-line program that stores university courses and their
prerequisites in an UNWEIGHTED DIRECTED GRAPH.

* Each vertex is a course.
* Each edge points FROM a prerequisite TO the course it unlocks,
  e.g. CS101 -> CS201 means CS101 must be passed before CS201.

Run this file to start the program.
"""


# ===========================================================================
# 1. GRAPH (unweighted, directed, stored as an adjacency list)
#    It contains no course-specific code, so it can be reused for any data.
# ===========================================================================
class Graph:
    """An unweighted directed graph. Vertices can be any kind of object."""

    def __init__(self):
        # Each vertex maps to a list of the vertices its edges point TO (outgoing edges)
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        """Add a new vertex. Returns False if it is already in the graph."""
        if vertex in self.adjacency_list:
            return False
        self.adjacency_list[vertex] = []          # a new vertex starts with no edges
        return True

    def has_vertex(self, vertex):
        return vertex in self.adjacency_list

    def get_vertices(self):
        """Return a list of every vertex, in the order they were added."""
        return list(self.adjacency_list)

    def vertex_count(self):
        return len(self.adjacency_list)

    def has_edge(self, from_vertex, to_vertex):
        """True if there is an edge from_vertex -> to_vertex."""
        return self.has_vertex(from_vertex) and to_vertex in self.adjacency_list[from_vertex]

    def add_edge(self, from_vertex, to_vertex):
        """Connect from_vertex -> to_vertex.
        Returns False if a vertex is missing or the edge already exists."""
        if not self.has_vertex(from_vertex) or not self.has_vertex(to_vertex):
            return False
        if self.has_edge(from_vertex, to_vertex):
            return False
        self.adjacency_list[from_vertex].append(to_vertex)
        return True

    def remove_edge(self, from_vertex, to_vertex):
        """Remove the edge from_vertex -> to_vertex. Returns False if it does not exist."""
        if not self.has_edge(from_vertex, to_vertex):
            return False
        self.adjacency_list[from_vertex].remove(to_vertex)
        return True

    def list_outgoing_adjacent_vertex(self, vertex):
        """Return every vertex that an edge goes TO from this vertex."""
        return list(self.adjacency_list[vertex])  # a copy, so the graph cannot be changed by accident

    def list_incoming_adjacent_vertex(self, vertex):
        """Return every vertex that has an edge coming INTO this vertex."""
        incoming = []
        for other_vertex in self.adjacency_list:            # check every vertex's list of edges
            if vertex in self.adjacency_list[other_vertex]:
                incoming.append(other_vertex)
        return incoming


# ---------------------------------------------------------------------------
# Quick test of the Graph on its own, using simple letters as vertices
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    graph = Graph()
    for letter in ["A", "B", "C", "D"]:
        graph.add_vertex(letter)
    graph.add_edge("A", "C")      # A -> C
    graph.add_edge("B", "C")      # B -> C
    graph.add_edge("C", "D")      # C -> D

    print("Vertices:", graph.get_vertices())
    print("Incoming to C:", graph.list_incoming_adjacent_vertex("C"))
    print("Outgoing from C:", graph.list_outgoing_adjacent_vertex("C"))
    print("Add A -> C again:", graph.add_edge("A", "C"))
    print("Remove A -> C:", graph.remove_edge("A", "C"))
    print("Incoming to C now:", graph.list_incoming_adjacent_vertex("C"))