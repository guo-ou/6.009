import json, traceback, os.path, random, copy, re
import pprint

try:
    import lab
except ImportError:
    import _solution as lab

try:
    reload(lab)
except NameError:
    # Python 3 compatibility
    import importlib
    importlib.reload(lab)

player_x = 0
def recenter_on_player(blobs,w):
    global player_x

    # find player, update player_x
    for b in blobs:
        if b['player']:
            player_x = b['rect'][0]
            break

    # put player in center of window
    adj = player_x - w//2
    for b in blobs:
        b['rect'][0] -= adj

def readmap(path):
    with open(path,'r') as txt:
        lines = [l.rstrip() for l in txt]
        width = max(map(len, lines))
        levelmap = [list(l.ljust(width, " ")) for l in lines]
        return levelmap

def record_trace(test, window, events):
    level = readmap(os.path.join("resources", "maps", test))
    game = lab.Game(level)
    yield copy.deepcopy(game.render(*window))
    for keys in events:
        game.timestep(keys)
        yield copy.deepcopy(game.render(*window))

def run_replay(test, window, events):
    return list(record_trace(test, window, events))

def rectangle(xmin, xmax, ymin, ymax):
    x, y = (random.randint(xmin, xmax), random.randint(ymin, ymax))
    xx, yy = (random.randint(xmin, xmax), random.randint(ymin, ymax))
    return [x, y, xx - x, yy - y]

def simple_rectangles():
    return [lab.Rectangle(0, 0, 128, 128),
            lab.Rectangle(-128, -128, 128, 128),
            lab.Rectangle(-64, -64, 128, 128)]

def partincluded(r1, r2):
    return (r1.x < r2.x < r2.x + r2.w < r1.x + r1.w or
            r1.y < r2.y < r2.y + r2.h < r1.y + r1.h)

def validpair(r1, r2):
    return ((not partincluded(r1, r2)) and
            (not partincluded(r2, r1)) and
            ((2 * r1.x + r1.w != 2 * r2.x + r2.w) or
             (2 * r1.y + r1.h != 2 * r2.y + r2.h)))

def iter_pairs(rects):
    for r1 in rects:
        for r2 in rects:
            if validpair(r1, r2):
                yield r1, r2
                yield r2, r1

def rectangle_pairs():
    random.seed(0)
    simple = simple_rectangles()
    randomized = [rectangle(-256, 256, -256, 256) for _ in range(250)]
    randomized = [lab.Rectangle(x, y, w, h) for (x, y, w, h) in randomized if w > 0 and h > 0]
    return list(iter_pairs(simple)) + list(iter_pairs(randomized))

def serialize_rect(r):
    return [r.x, r.y, r.w, r.h]

def run_intersection(test):
    return [(serialize_rect(r1), serialize_rect(r2), r1.intersects(r2))
            for r1, r2 in rectangle_pairs()]

def run_translationvector(test):
    return [(serialize_rect(r1), serialize_rect(r2), lab.Rectangle.translationvector(r1, r2))
            for r1, r2 in rectangle_pairs()]

def run_test(input_data):
    test_type = input_data.pop("type")
    try:
        testfn = {"replay": run_replay,
                  "intersection": run_intersection,
                  "translationvector": run_translationvector}[test_type]
        return ("result", testfn(**input_data))
    except NotImplementedError:
        return ("error", "Not implemented yet")
    except:
        return ("error", traceback.format_exc())

##################################################
## code used by server.py -- please don't break!
##################################################

class InstrumentedGame(object):
    def __init__(self, levelname):
        level = readmap(os.path.join('resources', 'maps', levelname))
        self.game = lab.Game(level)
        self.load_test_output(levelname)
        self.step = -1

    def load_test_output(self, levelname):
        m = re.match("w[12]-tests-0*([0-9]+)-", levelname)
        if not m:
            self.test_in_name = "<no .in file found>"
            self.test_out_name = "<no .out file found>"
            self.window = None
            self.ref_in, self.ref_out = [], []
            return
        self.test_in_name = os.path.join('cases', m.group(1) + ".in")
        self.test_out_name = os.path.join('cases', m.group(1) + ".out")
        with open(self.test_in_name) as ref_in:
            js_in = json.load(ref_in)
        with open(self.test_out_name) as ref_out:
            js_out = json.load(ref_out)
        self.window = js_in["window"]
        self.ref_in = js_in["events"]
        self.ref_out = js_out
        assert len(self.ref_in) + 1 == len(self.ref_out)

    def timestep(self, ghost_mode, actions):
        if ghost_mode:
            self.step += 1
            if self.step < len(self.ref_in):
                self.game.timestep(self.ref_in[self.step])
            else:
                print("No more input in {}".format(self.test_in_name))
        else:
            self.game.timestep([s.lower() for s in actions])

    @staticmethod
    def add_rect_field(blobs):
        for b in blobs:
            if "pos" in b:
                b["rect"] = list(b.pop("pos")) + [lab.Constants.TILE_SIZE, lab.Constants.TILE_SIZE]
        return blobs

    @staticmethod
    def adjust_blobs(blobs):
        assert all(("rect" in b or "pos" in b) and "texture" in b and "player" in b
                   for b in blobs)

        # adjust depending on leftmost floor tile
        floor_xs = [blob["rect"][0] for blob in blobs if blob["texture"] == '2b1b']
        floor_min_x = min(floor_xs) if floor_xs else 0
        for blob in blobs:
            blob["rect"][0] -= floor_min_x

    def render(self, ghost_mode, w, h):
        window = (self.window if ghost_mode else None) or (w, h)
        state, blobs = copy.deepcopy(self.game.render(*window))
        ref_state = None
        InstrumentedGame.add_rect_field(blobs)
        if ghost_mode:
            if self.step + 1 < len(self.ref_out):
                ref_state, ref = self.ref_out[self.step + 1]
                ref = copy.deepcopy(ref)
                refblobs = InstrumentedGame.add_rect_field(ref)
                # assert blobs == refblobs, pprint.pformat((self.step, (blobs, refblobs)))
                for blob in refblobs:
                    blob["ghost"] = True
                blobs += refblobs
            else:
                print("No more output in {}".format(self.test_out_name))
            InstrumentedGame.adjust_blobs(blobs)

        return [state, ref_state], blobs

current_game = None

# create a new game
def init_game(levelname):
    global player_x
    global current_game
    print('loading map: "%s"' % levelname)
    current_game = InstrumentedGame(levelname)
    player_x = 0
    return (len(current_game.ref_in) > 0)

# deliver the specified action to the game,
# render and return the resulting state,
def timestep(args):
    actions, ghost_mode, w, h = args
    current_game.timestep(ghost_mode, actions)
    status, result = current_game.render(ghost_mode, w, h)
    recenter_on_player(result,w)
    return status, result

# render and return the resulting state,
def render(args):
    ghost_mode, w, h = args
    status, result = current_game.render(ghost_mode,w,h)
    recenter_on_player(result,w)
    return status, result
