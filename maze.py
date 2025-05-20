from collections import deque
import sys


class Node:
    def __init__(self, state, parent, action):
        """
        Initializes a Node with the given state, parent, and action.

        :param state: The state of the node.
        :type state: object
        :param parent: The parent node leading to this node.
        :type parent: Node or None
        :param action: The action taken to reach this node.
        :type action: str or None
        """

        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    """Stack frontier for Deep First Search. (LIFO)"""

    def __init__(self):
        """
        Initializes the frontier as an empty queue.
        """

        self.frontier = deque()

    def add(self, node: Node):
        """
        Adds a node to the frontier.

        :param node: The node to add to the frontier.
        :type node: Node
        """
        return self.frontier.append(node)

    def contains_state(self, state):
        """
        Returns True if the given state is in the frontier, otherwise False.

        :param state: The state to check if in the frontier
        :type state: object
        :return: True if the state is in the frontier, otherwise False
        :rtype: bool
        """
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """
        Returns True if the frontier is empty, otherwise False.

        :return: True if the frontier is empty, otherwise False
        :rtype: bool
        """
        return len(self.frontier) == 0

    def remove(self):
        """
        Removes the last node from the frontier.

        :raises Exception: if the frontier is empty.
        :return: the last node in the frontier
        :rtype: Node
        """
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop()  # removes and return that last item in the list


class QueueFrontier(StackFrontier):
    """Queue frontier for Breadth First Search. (FIFO)"""

    def remove(self):
        """
        Overrides the remove method from StackFrontier.

        Removes the first node from the frontier.

        :raises Exception: if the frontier is empty.
        :return: the first node in the frontier
        :rtype: Node
        """
        if self.empty():
            raise Exception("empty frontier")
        else:
            return (
                self.frontier.popleft()
            )  # removes and return the first item in the list


class Maze:
    def __init__(self, filename):
        """
        Initializes the Maze object by reading the maze configuration from a file.

        The maze is represented as a grid of cells, where each cell can be a wall,
        the start point 'A', the goal point 'B', or an empty space. The function
        reads the maze from the specified file, validates the presence of exactly
        one start and one goal, and sets the height and width of the maze. It also
        tracks the positions of walls, start, and goal within the maze.

        :param filename: The name of the file containing the maze configuration.
        :type filename: str
        :raises Exception: If the maze does not contain exactly one start point or
                        one goal point.
        """

        with open(filename) as f: # open the file
            contents = f.read() # read the file

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents = contents.splitlines() # divide the contentes into lines of the maze.
        self.height = len(contents)  # determines the height of the maze
        self.width = max(
            len(line) for line in contents
        )  # determines the width of the maze

        contents = [line.ljust(self.width) for line in contents] # makes sure that all lines have the same width

        self.walls = [] # creates a list to store the walls (True for a wall, False for a blank space) 
        for i in range(self.height): # iterates over the rows
            row = []
            for j in range(self.width): # iterates over the columns
                cell = contents[i][j]
                if cell in ("A", "B", " "): # checks if the cell is a wall
                    row.append(False)
                    if cell == "A":
                        self.start = (i, j)
                    elif cell == "B":
                        self.goal = (i, j)
                else:
                    row.append(True)
            self.walls.append(row)

        self.solution = None

    def print(self):
        """
        Prints a simple text representation of the maze, with the start (A),
        goal (B), and any solution path marked.

        :return: None
        """
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):  # iterates over the rows
            for j, col in enumerate(row):  # iterates over the columns
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        """
        Returns a list of valid neighboring states from the given state along with the actions
        required to reach them. A neighboring state is considered valid if it is within the
        maze's boundaries and not a wall.

        :param state: The current position in the maze, represented as a tuple (row, col).
        :type state: tuple
        :return: A list of tuples, each containing an action ("up", "down", "left", "right")
                and the resulting neighboring state as a tuple (row, col).
        :rtype: list
        """

        row, col = state  # unpacks the state tuple

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]  # list of tuples containing the action and the resulting neighboring state

        result = []
        for action, (r, c) in candidates:
            if (
                0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]
            ):  # if the neighbor is within the maze's boundaries and not a wall
                result.append((action, (r, c)))
        return result

    def solve(self, method="dfs"):
        """
        Solves the maze using the specified search method.

        :param method: The search method to use (default is "dfs")
        :type method: str
        :raises Exception: If the maze cannot be solved
        :return: None
        """
        self.num_explored = 0
        start = Node(
            state=self.start, parent=None, action=None
        )  # defines the initial state

        if method == "bfs":
            frontier = QueueFrontier()
        else:
            frontier = StackFrontier()

        frontier.add(start)  # adds the initial state to the frontier

        self.explored = set()  # keeps track of the states that have been explored

        while True:
            if frontier.empty():
                raise Exception("No solution")

            node = (
                frontier.remove()
            )  # removes the first or the last (depending on the method) node from the frontier
            self.num_explored += (
                1  # increments the number of states that have been explored
            )

            if node.state == self.goal:  # if the goal state has been reached
                actions = []
                cells = []
                while (
                    node.parent is not None
                ):  # adds the actions and the cells to the solution
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()  # reverses the lists (this happens because the solution is reversed)
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)  # adds the state to the explored set

            for action, state in self.neighbors(
                node.state
            ):  # adds the neighbors to the frontier
                if (
                    not frontier.contains_state(state) and state not in self.explored
                ):  # if the neighbor is not in the frontier and not in the explored set
                    child = Node(state=state, parent=node, action=action)

                    frontier.add(child)  # adds the child node to the frontier


m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve(method="bfs")
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
