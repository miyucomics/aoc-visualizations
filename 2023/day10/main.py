import colors
from blessed import Terminal

with open("input.txt") as file:
    world = file.read()
    world_width = len(world.split("\n")[0])
    world_height = world.count("\n")
    world = world.replace("\n", "")
def get(x, y):
    if x < 0 or x >= world_width or y < 0 or y >= world_height:
        return "OFFSCREEN"
    return world[y * world_width + x]


def print_char(x, y, char):
    print(term.move_xy(x, y) + char, end="", flush=True)

moves = {
    (0, -1): lambda a, b: a in "S|LJ" and b in "S|F7",  # up
    (0, 1): lambda a, b: a in "S|F7" and b in "S|LJ",  # down
    (-1, 0): lambda a, b: a in "S-J7" and b in "S-LF",  # left
    (1, 0): lambda a, b: a in "S-LF" and b in "S-J7"  # right
}

mapping = { "S": "S", "7": "┐", "J": "┘", "F": "┌", "L": "└", "|": "│", "-": "─" }

starty, startx = divmod(world.index("S"), world_width)
last_x = x = startx
last_y = y = starty
distance = 0
visited = [(startx, starty)]

term = Terminal()
with term.cbreak(), term.hidden_cursor(), term.fullscreen():
    print(term.home + term.on_color_rgb(*colors.crust) + term.clear)

    print(term.color_rgb(*colors.surface0))
    for i, char in enumerate(world):
        print_char(i % world_width + 2, int(i / world_width + 1), char)

    running = True
    while running and term.inkey(timeout=0.01) != "q":
        for move, check in moves.items():
            new_x = x + move[0]
            new_y = y + move[1]
            if new_x == last_x and new_y == last_y:
                continue
            if check(get(x, y), get(new_x, new_y)):
                print(term.color_rgb(*colors.blue))
                print_char(x + 2, y + 1, mapping[get(x, y)])
                last_x = x
                last_y = y
                x = new_x
                y = new_y
                visited.append((x, y))
                distance += 1
                if x == startx and y == starty:
                    running = False
                print(term.color_rgb(*colors.green) + term.bold)
                for i, char in enumerate("Distance: " + str(distance)):
                    print_char(world_width + 3 + i, 1, char)
                print(term.color_rgb(*colors.red) + term.bold)
                for i, char in enumerate("Furthest Distance: " + str(distance / 2)):
                    print_char(world_width + 3 + i, 3, char)
                break

    print(term.color_rgb(*colors.red) + term.bold)
    for i in range(int(distance / 2) - 1):
        print_char(visited[i][0] + 2, visited[i][1] + 1, mapping[get(visited[i][0], visited[i][1])])
        term.inkey(timeout=0.05)
    print_char(visited[int(distance / 2) - 1][0] + 2, visited[int(distance / 2) - 1][1] + 1, "X")

    while term.inkey(timeout=0.05) != "q":
        ...
