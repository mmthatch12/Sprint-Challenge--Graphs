from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

class Graph:
    def __init__(self):
        # vertices
        # do I need a counter to keep track of all added rooms?
        self.rooms_count = 0
        self.rooms = {}
    def add_room(self, room):
        # add vertex to the graph with dictionary as value
        if room not in self.rooms:
            directions_list = player.current_room.get_exits()
            directions = {}
            for direct in directions_list:
                directions[direct] = '?'
            self.rooms[room] = directions
            self.rooms_count +=1
        else:
            print(f"room: {room} already exists, did not add.")
            return False
    def connect_rooms(self, room):
        dir_list = []
        for direction in self.rooms[room]:
            if self.rooms[room][direction] == '?':
                dir_list.append(direction)
        random.shuffle(dir_list)
        next_dir = dir_list.pop()
        player.travel(next_dir)
        traversal_path.append(next_dir)
        for direction in self.rooms[room]:
            if direction == next_dir:
                self.rooms[room][direction] = player.current_room.id
        if player.current_room.id not in self.rooms:
            self.add_room(player.current_room.id)
            for direction in self.rooms[player.current_room.id]:
                if next_dir == 'n':
                    self.rooms[player.current_room.id]['s'] = room
                if next_dir == 's':
                    self.rooms[player.current_room.id]['n'] = room
                if next_dir == 'e':
                    self.rooms[player.current_room.id]['w'] = room
                if next_dir == 'w':
                    self.rooms[player.current_room.id]['e'] = room
        else:
            for direction in self.rooms[player.current_room.id]:
                if next_dir == 'n':
                    self.rooms[player.current_room.id]['s'] = room
                if next_dir == 's':
                    self.rooms[player.current_room.id]['n'] = room
                if next_dir == 'e':
                    self.rooms[player.current_room.id]['w'] = room
                if next_dir == 'w':
                    self.rooms[player.current_room.id]['e'] = room
        return player.current_room.id

    def dft(self, starting_room):
        stack = Stack()
        stack.push([starting_room])

        visited = []

        while stack.size() > 0:

            room = stack.pop()
            visited.append(room)
            self.connect_rooms(room)

            # if room not in visited:
                
            # visited[room] = new_path

            # for roo in self.rooms[room]:
                # path_copy = new_path.copy()
                # path_copy.append(roo)
                # stack.push(path_copy)
    
    def bfs(self, room_id):

        visited = {}

        queue = Queue()

        queue.enqueue([room_id])

        while queue.size() > 0:
            new_path = queue.dequeue()
            room = new_path[-1]

            if room not in visited:
                visited[room] = new_path

                for roo in self.rooms[room]:
                    path_copy = new_path.copy()
                    path_copy.append(roo)
                    queue.enqueue(path_copy)



# Start by writing an algorithm that picks a random unexplored direction from the 
# player's current room, travels and logs that direction, then loops. This should
# cause your player to walk a depth-first traversal. When you reach a 
# dead-end (i.e. a room with no unexplored paths), walk back to the nearest 
# room that does contain an unexplored path.
        

tg = Graph()
tg.add_room(player.current_room.id)
tg.connect_rooms(player.current_room.id)
print("----printing rooms test")
print(tg.rooms)


#You can find the path to the shortest unexplored room by using a 
# breadth-first search for a room with '?' for an exit. If you use the 
# bfs code from the homework, you will need to make a few modifications
#   




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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
