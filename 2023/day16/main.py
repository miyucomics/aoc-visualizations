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

mirrors = {
    "/": {(1, 0): (0, -1), (-1, 0): (0, 1), (0, 1): (-1, 0), (0, -1): (1, 0)},
    "\\": {(1, 0): (0, 1), (-1, 0): (0, -1), (0, 1): (1, 0), (0, -1): (-1, 0)}
}
splitters = {
    "|": {(1, 0): [(0, -1), (0, 1)], (-1, 0): [(0, -1), (0, 1)], (0, 1): [(0, 1)], (0, -1): [(0, -1)]},
    "-": {(1, 0): [(1, 0)], (-1, 0): [(-1, 0)], (0, 1): [(1, 0), (-1, 0)], (0, -1): [(1, 0), (-1, 0)]}
}

class Beam:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

beams = []
energized_tiles = set()
cache = set()

beams.append(Beam(0, 0, 1, 0))

term = Terminal()

with term.cbreak(), term.hidden_cursor(), term.fullscreen():
    print(term.home + term.on_color_rgb(*colors.crust) + term.clear)

    print(term.color_rgb(*colors.surface1))
    for i, char in enumerate(world):
        print_char(i % world_width + 2, int(i / world_width + 1), char)

    times_reflected = 0
    times_split = 0
    while beams:
        beam = beams.pop()
        while get(beam.x, beam.y) != "OFFSCREEN":
            print(term.color_rgb(*colors.yellow) + term.bold)
            energized_tiles.add((beam.x, beam.y))

            iota = get(beam.x, beam.y)
            if iota in mirrors.keys():
                beam.dx, beam.dy = mirrors[iota][(beam.dx, beam.dy)]
                times_reflected += 1
            if iota in splitters.keys():
                if (beam.x, beam.y, beam.dx, beam.dy) in cache:
                    break
                cache.add((beam.x, beam.y, beam.dx, beam.dy))
                new_beams = splitters[iota][(beam.dx, beam.dy)]
                beam.dx, beam.dy = new_beams[0]
                if len(new_beams) == 2:
                    beams.insert(0, Beam(beam.x, beam.y, new_beams[1][0], new_beams[1][1]))
                    times_split += 1

            beam.x += beam.dx
            beam.y += beam.dy

            if get(beam.x, beam.y) == ".":
                if (beam.x, beam.y) in energized_tiles:
                    print_char(beam.x + 2, beam.y + 1, "+")
                elif beam.dx == 0:
                    print_char(beam.x + 2, beam.y + 1, "|")
                else:
                    print_char(beam.x + 2, beam.y + 1, "-")

            for i, char in enumerate("Energized tiles: " + str(len(energized_tiles))):
                print_char(115 + i, 1, char)

            print(term.color_rgb(*colors.blue) + term.bold)
            for i, char in enumerate("Reflected: " + str(times_reflected)):
                print_char(115 + i, 3, char)

            print(term.color_rgb(*colors.red) + term.bold)
            for i, char in enumerate("Split: " + str(times_split)):
                print_char(115 + i, 5, char)

            print(term.color_rgb(*colors.green) + term.bold)
            for i, char in enumerate("Cued beams: " + str(len(beams)).rjust(3, "0")):
                print_char(115 + i, 7, char)

            if term.inkey(timeout=0.01) == "q":
                exit()

    while term.inkey(timeout=0.05) != "q":
        ...
