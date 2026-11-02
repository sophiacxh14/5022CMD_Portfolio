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


# ===========================================================================
# 2. ENTITY CLASS
# ===========================================================================
class Course:
    """One course offered by the university."""

    def __init__(self, code, name, credit_hours, level, year, description):
        self.code = code                    # str - unique course code, e.g. "CS201"
        self.name = name                    # str - e.g. "Data Structures"
        self.credit_hours = credit_hours    # int - e.g. 4
        self.level = level                  # str - "Core" or "Elective"
        self.year = year                    # int - year of study (1 to 3)
        self.description = description      # str - short summary of the course

    def is_core(self):
        return self.level == "Core"

    def __str__(self):
        """Short form used in lists, e.g. 'CS201 - Data Structures'."""
        return f"{self.code} - {self.name}"


# ===========================================================================
# 3. PRE-DEFINED COURSES AND PREREQUISITES
# ===========================================================================
def load_sample_data(graph):
    """Create 8 courses (vertices) and their prerequisite links (edges)."""
    cs101 = Course("CS101", "Programming Fundamentals", 4, "Core", 1,
                   "Basic programming with variables, loops, functions and lists.")
    cs102 = Course("CS102", "Discrete Mathematics", 3, "Core", 1,
                   "Logic, sets, counting and graph theory for computing.")
    cs201 = Course("CS201", "Data Structures", 4, "Core", 2,
                   "Arrays, linked lists, stacks, queues, trees and hash tables.")
    cs202 = Course("CS202", "Database Systems", 3, "Core", 2,
                   "Relational databases, SQL and database design.")
    cs301 = Course("CS301", "Advanced Algorithms", 4, "Core", 3,
                   "Algorithm analysis, graphs, hashing and concurrency.")
    cs302 = Course("CS302", "Software Engineering", 4, "Core", 3,
                   "Requirements, design, testing and team projects.")
    cs303 = Course("CS303", "Artificial Intelligence", 3, "Elective", 3,
                   "Search, knowledge representation and machine learning basics.")
    cs304 = Course("CS304", "Web Development", 3, "Elective", 3,
                   "Building dynamic websites with a database back end.")

    for course in [cs101, cs102, cs201, cs202, cs301, cs302, cs303, cs304]:
        graph.add_vertex(course)

    # Each edge points FROM the prerequisite TO the course it unlocks
    graph.add_edge(cs101, cs201)
    graph.add_edge(cs101, cs202)
    graph.add_edge(cs201, cs301)
    graph.add_edge(cs102, cs301)
    graph.add_edge(cs201, cs302)
    graph.add_edge(cs202, cs302)
    graph.add_edge(cs301, cs303)
    graph.add_edge(cs202, cs304)


# ---------------------------------------------------------------------------
# Quick test: load the courses and show every prerequisite link
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    graph = Graph()
    load_sample_data(graph)

    print(f"Loaded {graph.vertex_count()} courses:")
    for course in graph.get_vertices():
        print(f"  {course} ({course.level}, Year {course.year}, {course.credit_hours} credit hours)")

    print("\nPrerequisite links (prerequisite -> course it unlocks):")
    for course in graph.get_vertices():
        for unlocked in graph.list_outgoing_adjacent_vertex(course):
            print(f"  {course.code} -> {unlocked.code}")