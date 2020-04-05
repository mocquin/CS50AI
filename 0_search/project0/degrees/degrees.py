import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    # association id/name/birthyear
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(directory +"/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    
    
    Complete the implementation of the shortest_path function 
    such that it returns the shortest path from the person with 
    id source to the person with the id target.

    Assuming there is a path from the source to the target, your 
    function should return a list, where each list item is the 
    next (movie_id, person_id) pair in the path from the source 
    to the target. Each pair should be a tuple of two ints.
    
    For example, if the return value of shortest_path were 
    [(1, 2), (3, 4)], that would mean that the source starred in
    movie 1 with person 2, person 2 starred in movie 3 with person 
    4, and person 4 is the target.
    If there are multiple paths of minimum length from the source 
    to the target, your function can return any of them.
    If there is no possible path between two actors, your function 
    should return None.
    You may call the neighbors_for_person function, which accepts a 
    person’s id as input, and returns a set of (movie_id, person_id) 
    pairs for all people who starred in a movie with a given person.

    You should not modify anything else in the file other than 
    the shortest_path function, though you may write additional 
    functions and/or import other Python standard library modules.
        
    
    """
    # read inputs
    source_id = source
    target_id = target
    # Initialize source node
    source_node = Node(state=source_id,
                       parent=None,
                       action=None)
    # Initialize Frontier with source node
    frontier = QueueFrontier()
    frontier.add(source_node)
    
    # Initialize explored set
    explored_nodes = set()
    num_explored = 0
    
    # keep looping until solution found
    while True:
        
        # If nothing left in frontier, then no path
        if frontier.empty():
            return None
            
        # Choose a node from the frontier
        node = frontier.remove() # and remove it
        num_explored += 1
        
        # If node is the goal, then we have a solution
        if node.state == target_id:
            # looping back from target to source
            actions = []
            cells = []    
            # only source_node has None as parent
            while node.parent is not None: 
                # add current node action to actions
                actions.append(node.action)
                # add current node state
                cells.append(node.state)
                # change node by taking parent node
                node = node.parent
            # sort actions and states 
            actions.reverse()
            cells.reverse()
            # return solution
            return [(action, cell) for action, cell in zip(actions, cells)]
        
        # else, node is not a solution
        # Mark node as explored ...
        explored_nodes.add(node.state)
        # ... and add neighbors to frontier
        # get action and state of current node
        for action, state in neighbors_for_person(node.state):
            # if state not already in frontier and not already explored
            if not frontier.contains_state(state) and state not in explored_nodes:
                # create note for that state
                # current node as parent
                # and action as action
                child = Node(state=state,
                             parent=node,
                             action=action)
                # add that child to the frontier
                frontier.add(child)

        

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
