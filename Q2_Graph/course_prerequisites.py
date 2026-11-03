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

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
MAX_COURSES = 10        # the brief allows a maximum of 10 courses


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
        return list(self.adjacency_list)          # list() of a dictionary gives its keys (the vertices)

    def vertex_count(self):
        return len(self.adjacency_list)

    def has_edge(self, from_vertex, to_vertex):
        """True if there is an edge from_vertex -> to_vertex."""
        # has_vertex() is checked first, so a missing vertex returns False instead of crashing
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

    def has_path(self, start, target):
        """True if target can be reached from start by following edges.
        Uses depth-first search: keep following edges until there is nowhere new to go."""
        visited = []                                  # vertices already checked, so none is checked twice
        to_visit = [start]                            # vertices still waiting to be checked
        while len(to_visit) > 0:
            current = to_visit.pop()                  # take the most recently added vertex
            if current == target:
                return True
            if current not in visited:
                visited.append(current)
                for next_vertex in self.adjacency_list[current]:
                    to_visit.append(next_vertex)      # follow every outgoing edge
        return False


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


# ===========================================================================
# 4. HELPER FUNCTIONS
# ===========================================================================
def find_course(graph, code) -> Course | None:
    """Return the Course with this code (any letter case), or None if there is none."""
    for course in graph.get_vertices():
        if course.code == code.strip().upper():  # so "cs301" and " CS301 " also match
            return course
    return None


def ask_for_course(graph, prompt) -> Course | None:
    """Ask for a course code. Returns the Course, or None (with a message) if not found."""
    code = input(prompt).strip().upper()
    course = find_course(graph, code)
    if course is None:
        print(f"  Course '{code}' not found. Use option 1 to see all course codes.")
    return course


def course_codes(courses):
    """Turn a list of courses into text such as 'CS201, CS102', or 'None' if empty."""
    if len(courses) == 0:
        return "None"
    codes = []
    for course in courses:
        codes.append(course.code)
    return ", ".join(codes)        # put ", " between the codes, e.g. "CS102, CS201"


def print_course_list(title, courses):
    """Print a heading and one course per line, or 'None' if the list is empty."""
    print(title)
    if len(courses) == 0:
        print("  - None")
    for course in courses:
        print(f"  - {course.code} ({course.name})")


def print_full_details(graph, course):
    """Print every attribute of a course, plus its prerequisites and the courses it unlocks."""
    prerequisites = graph.list_incoming_adjacent_vertex(course)
    unlocks = graph.list_outgoing_adjacent_vertex(course)
    print(f"  Course Code   : {course.code}")
    print(f"  Course Name   : {course.name}")
    print(f"  Credit Hours  : {course.credit_hours}")
    print(f"  Level         : {course.level}")
    print(f"  Year of Study : {course.year}")
    print(f"  Description   : {course.description}")
    print(f"  Prerequisites : {course_codes(prerequisites)}")
    print(f"  Unlocks       : {course_codes(unlocks)}")


# ===========================================================================
# 5. MENU OPTIONS - MANDATORY FEATURES
# ===========================================================================
def view_all_courses(graph):
    print(f"\nAvailable Courses ({graph.vertex_count()} of {MAX_COURSES}):")
    number = 1
    for course in graph.get_vertices():
        print(f"  {number}. {course}")
        number += 1


def view_course_details(graph):
    print("\n--- View Course Details ---")
    course = ask_for_course(graph, "Enter Course Code: ")
    if course is not None:
        print_full_details(graph, course)       # all information, whatever the level


def view_prerequisites(graph):
    print("\n--- View Prerequisites of a Course ---")
    course = ask_for_course(graph, "Enter Course Code: ")
    if course is not None:
        prerequisites = graph.list_incoming_adjacent_vertex(course)   # INCOMING edges
        print_course_list(f"Prerequisites for {course}:", prerequisites)


def view_unlocked_courses(graph):
    print("\n--- View Courses Unlocked by a Course ---")
    course = ask_for_course(graph, "Enter Course Code: ")
    if course is not None:
        unlocked = graph.list_outgoing_adjacent_vertex(course)        # OUTGOING edges
        print_course_list(f"Courses unlocked by {course}:", unlocked)


# ===========================================================================
# 6. MENU OPTIONS - ADVANCED FEATURES
# ===========================================================================
def read_text(prompt):
    """Keep asking until the user types something that is not empty."""
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("  This field cannot be empty.")


def read_int(prompt, minimum, maximum):
    """Keep asking until the user types a whole number from minimum to maximum."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and minimum <= int(text) <= maximum:   # a whole number inside the range
            return int(text)
        print(f"  Please enter a whole number from {minimum} to {maximum}.")


def view_course_profile(graph):
    """Core courses show every detail; elective courses show only their name."""
    print("\n--- View Course Profile ---")
    course = ask_for_course(graph, "Enter Course Code: ")
    if course is None:
        return
    if course.is_core():
        print_full_details(graph, course)
    else:
        print(f"  Course Name   : {course.name}")
        print("  (Elective course: other details are hidden.)")


def add_course(graph):
    print("\n--- Add a Course ---")
    if graph.vertex_count() >= MAX_COURSES:      # checked first, so the user does not type details for nothing
        print(f"  The system already has the maximum of {MAX_COURSES} courses.")
        return

    code = read_text("Enter Course Code: ").upper()
    if find_course(graph, code) is not None:
        print(f"  Course {code} already exists.")
        return
    name = read_text("Enter Course Name: ")
    credit_hours = read_int("Enter Credit Hours (1-6): ", 1, 6)
    level_choice = read_int("Enter Level (1 = Core, 2 = Elective): ", 1, 2)
    level = "Core" if level_choice == 1 else "Elective"   # choosing a number avoids spelling mistakes
    year = read_int("Enter Year of Study (1-3): ", 1, 3)
    description = read_text("Enter Description: ")

    graph.add_vertex(Course(code, name, credit_hours, level, year, description))   # new vertex
    print(f"  Course {code} - {name} added successfully. "
          f"Use option 7 to give it prerequisites.")


def add_prerequisite(graph):
    print("\n--- Add a Prerequisite ---")
    course = ask_for_course(graph, "Enter the Course Code that needs a prerequisite: ")
    if course is None:
        return
    prerequisite = ask_for_course(graph, "Enter the Prerequisite Course Code: ")
    if prerequisite is None:
        return

    # Read the codes once, for use in the messages below
    course_code = course.code
    prerequisite_code = prerequisite.code

    if prerequisite == course:
        print("  A course cannot be a prerequisite of itself.")
    elif graph.has_edge(prerequisite, course):
        print(f"  {prerequisite_code} is already a prerequisite of {course_code}.")
    elif graph.has_path(course, prerequisite):
        # course already leads to prerequisite, so an edge back would create a loop
        print(f"  Not allowed: {prerequisite_code} already depends on {course_code}, "
              f"so this would create a prerequisite loop.")
    else:
        graph.add_edge(prerequisite, course)     # new edge FROM prerequisite TO course
        print(f"  {prerequisite_code} is now a prerequisite of {course_code}.")


def remove_prerequisite(graph):
    print("\n--- Remove a Prerequisite ---")
    course = ask_for_course(graph, "Enter the Course Code: ")
    if course is None:
        return
    prerequisite = ask_for_course(graph, "Enter the Prerequisite Course Code to remove: ")
    if prerequisite is None:
        return

    if graph.remove_edge(prerequisite, course):  # remove the edge FROM prerequisite TO course
        print(f"  {prerequisite.code} is no longer a prerequisite of {course.code}.")
    else:
        print(f"  {prerequisite.code} is not a prerequisite of {course.code}.")


# ===========================================================================
# 7. MAIN PROGRAM
# ===========================================================================
def main():
    graph = Graph()
    load_sample_data(graph)
    print(f"Loaded {graph.vertex_count()} courses.")

    while True:
        print("\n==== University Course Prerequisite System ====")
        print("1. View All Courses")
        print("2. View Course Details")
        print("3. View Prerequisites of a Course")
        print("4. View Courses Unlocked by a Course")
        print("5. View Course Profile (electives show name only)")
        print("6. Add a Course")
        print("7. Add a Prerequisite")
        print("8. Remove a Prerequisite")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_all_courses(graph)
        elif choice == "2":
            view_course_details(graph)
        elif choice == "3":
            view_prerequisites(graph)
        elif choice == "4":
            view_unlocked_courses(graph)
        elif choice == "5":
            view_course_profile(graph)
        elif choice == "6":
            add_course(graph)
        elif choice == "7":
            add_prerequisite(graph)
        elif choice == "8":
            remove_prerequisite(graph)
        elif choice == "0":
            print("Exiting program. Goodbye!")
            break
        else:
            print("  Invalid choice. Please enter a number from the menu.")


# Run the menu only when this file is executed directly, not when it is imported.
if __name__ == "__main__":
    main()