from pylint import graph

from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n', 's', 'w','w','w','s','w','s']
# directions represented by a string of 'n' 's' 'e' 'w'
traversal_path = []

# this is for retracing your steps when hitting a dead end
reverse_path = []

# create a dict to keep track of the rooms that have been visited
# {room.id : [exits dir]} that is how the txt files are set up
visited = {}

# map of counter opposite directions to retrace steps
rev_dir = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
    }

# start to insert in visited - {room.id: [exits dir]}
# use get_exits() from Room class
visited[player.current_room.id] = player.current_room.get_exits()
# while the length of the visited is less than the length of the total amount of rooms
# to not count the starting location, - 1 to the graph
while len(visited) < len(room_graph) - 1:
    # if the room where you're at isn't in visited
    if player.current_room.id not in visited:
        # add it to visited with its id and [] of exits dir. It needs to be able to be modified
        visited[player.current_room.id] = player.current_room.get_exits()
        # you need to be able to go backwards so you can grab the previous dir
        # grab it from the end of the reverse path
        prev_dir = reverse_path[-1]
        # visual on XD file
        visited[player.current_room.id].remove(prev_dir)

    # while you hit a dead end and you have no where to go no exits
    while len(visited[player.current_room.id]) == 0:
        # find the last exit dir from reverse_path into the variable prev_dir
        prev_dir = reverse_path.pop()
        # add this dir to the traversal_path because it is part of the entire path
        traversal_path.append(prev_dir)
        # now you have to move the player to the last room that still has options for dir
        # with the travel function found in player
        player.travel(prev_dir)

    # Now that the current rooms are visited and you're not at a dead end
    # grab the new (numeric order) dir from the current room that you are in
    move_dir = visited[player.current_room.id].pop(0)
    # now add it to the traversal_path
    traversal_path.append(move_dir)
    # add the reverse dir to the reverse_path
    reverse_path.append(rev_dir[move_dir])

    # TRAVERSAL TEST
    visited_rooms = set()
    player.current_room = world.starting_room
    visited_rooms.add(player.current_room)

    for move in traversal_path:
        player.travel(move)
        visited_rooms.add(player.current_room)

    if len(visited_rooms) == len(room_graph):
        print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
    else:
        print("TESTS FAILED: INCOMPLETE TRAVERSAL")
        print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

    #######
    # UNCOMMENT TO WALK AROUND
    #######
    # player.current_room.print_room_description(player)
    # while True:
    #     cmds = input("-> ").lower().split(" ")
    #     if cmds[0] in ["n", "s", "e", "w"]:
    #         player.travel(cmds[0], True)
    #     elif cmds[0] == "q":
    #         break
    #     else:
    #         print("I did not understand that command.")
