from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
view_stack = []
view_queue = []
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
    def connect_rooms(self, next_dir, curr_room, prev_room):
        for direction in self.rooms[prev_room]:
            if direction == next_dir:
                self.rooms[prev_room][direction] = curr_room
        for direction in self.rooms[curr_room]:
            if next_dir == 'n':
                self.rooms[curr_room]['s'] = prev_room
            if next_dir == 's':
                self.rooms[curr_room]['n'] = prev_room
            if next_dir == 'e':
                self.rooms[curr_room]['w'] = prev_room
            if next_dir == 'w':
                self.rooms[curr_room]['e'] = prev_room

    def dft_rand(self):
        stack = Stack()
        stack.push(player.current_room)
        view_stack.append(player.current_room.id)
        # print('initial view stack', view_stack)

        random_dir = None
        prev_room = None

        while len(self.rooms) <= len(room_graph): 
            curr_room = stack.pop()
            view_stack.pop()
            # print('view stack after pop', view_stack)
            if curr_room.id not in self.rooms:
                self.add_room(curr_room.id)     
                # print(curr_room.id, 'added to self.rooms')          

            if random_dir is None:
                dir_list =[]
                for direction in self.rooms[curr_room.id]:
                    if self.rooms[curr_room.id][direction] == '?':
                        dir_list.append(direction)
                    random.shuffle(dir_list)
                    random_dir = dir_list.pop()
            if prev_room is not None:
                self.connect_rooms(random_dir, curr_room.id, prev_room.id)
                # print(curr_room.id, "connected to", prev_room.id)

            if random_dir not in self.rooms[curr_room.id]:
                # print('random_dir', random_dir, 'self.rooms[curr_room.id]:', self.rooms[curr_room.id])
                unex_list = []
                
                for key, value in self.rooms[curr_room.id].items():
                    if value == '?':
                        unex_list.append(key)
                # print('unex_list', unex_list)
                if len(unex_list) == 0:
                    path = self.bfs(curr_room)
                    # print('path', path)
                    if path is None:
                        # print('path is none')
                        return 
                    new_room = path[-1][0]
                    # print('path[-1][0]', path[-1][0])
                    for move in path[1:]:
                        traversal_path.append(move[1])
                        player.travel(move[1])
                        # print('player.current_room bfs', player.current_room.id)

                    unex_list = []
                    for key, value in self.rooms[new_room].items():
                        if value == '?':
                            unex_list.append(key)
                    random.shuffle(unex_list)
                random_dir = unex_list.pop()

            traversal_path.append(random_dir)
            prev_room = player.current_room
            player.travel(random_dir)
            # print('player.current_room dft', player.current_room.id)
            stack.push(player.current_room)
            view_stack.append(player.current_room.id)
            # print('from outer cond of dft viewstack', view_stack) 
    
    def bfs(self, first_room):
        queue = Queue()
        queue.enqueue([(first_room.id, "")])
        view_queue.append([(first_room.id, "")])
        # print('initial view_queue', view_queue)

        visited_set = set()
        while queue.size() > 0 and len(self.rooms) < len(room_graph):
            new_path = queue.dequeue()
            view_queue.pop(0)
            # print('view_queue after dequeue', view_queue)
            room = new_path[-1][0]
            # print('room', room, 'new_path', new_path, 'queue', queue)
            for direction, value in self.rooms[room].items():
                if value == '?':
                    # print('all of room props:', self.rooms[room])
                    return new_path
            if room not in visited_set:
                visited_set.add(room)
                for direction, neighbor in self.rooms[room].items():
                    if neighbor not in visited_set:
                        next_path = list(new_path)
                        next_path.append((neighbor, direction))
                        queue.enqueue(next_path)
                        view_queue.append(next_path)
                        # print('viewqueue after append', view_queue)
                        # print('visited_set', visited_set)

        
tg = Graph()
tg.dft_rand()



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
