import copy 
import typing

import numpy as np 

PieceType = int 
PIECE_TYPES = [
    O1, I2, L3, I3, I4, L4, Z4, O4, T4, F5, I5, L5, N5, P5, T5, U5, V5, W5, X5, Y5, Z5
] = range(21) 

PIECE_NAMES = [
    "O1", "I2", "L3", "I3", "I4", "L4", "Z4", "O4", "T4", "F5", "I5", "L5", "N5", "P5", "T5", "U5", "V5", "W5", "X5", "Y5", "Z5"
]

Tile = int 
TILES = [
    A01, B01, C01, D01, E01, F01, G01, H01, I01, J01, K01, L01, M01, N01, O01, P01, Q01, R01, S01, T01, 
    A02, B02, C02, D02, E02, F02, G02, H02, I02, J02, K02, L02, M02, N02, O02, P02, Q02, R02, S02, T02, 
    A03, B03, C03, D03, E03, F03, G03, H03, I03, J03, K03, L03, M03, N03, O03, P03, Q03, R03, S03, T03, 
    A04, B04, C04, D04, E04, F04, G04, H04, I04, J04, K04, L04, M04, N04, O04, P04, Q04, R04, S04, T04, 
    A05, B05, C05, D05, E05, F05, G05, H05, I05, J05, K05, L05, M05, N05, O05, P05, Q05, R05, S05, T05, 
    A06, B06, C06, D06, E06, F06, G06, H06, I06, J06, K06, L06, M06, N06, O06, P06, Q06, R06, S06, T06, 
    A07, B07, C07, D07, E07, F07, G07, H07, I07, J07, K07, L07, M07, N07, O07, P07, Q07, R07, S07, T07, 
    A08, B08, C08, D08, E08, F08, G08, H08, I08, J08, K08, L08, M08, N08, O08, P08, Q08, R08, S08, T08, 
    A09, B09, C09, D09, E09, F09, G09, H09, I09, J09, K09, L09, M09, N09, O09, P09, Q09, R09, S09, T09, 
    A10, B10, C10, D10, E10, F10, G10, H10, I10, J10, K10, L10, M10, N10, O10, P10, Q10, R10, S10, T10, 
    A11, B11, C11, D11, E11, F11, G11, H11, I11, J11, K11, L11, M11, N11, O11, P11, Q11, R11, S11, T11, 
    A12, B12, C12, D12, E12, F12, G12, H12, I12, J12, K12, L12, M12, N12, O12, P12, Q12, R12, S12, T12, 
    A13, B13, C13, D13, E13, F13, G13, H13, I13, J13, K13, L13, M13, N13, O13, P13, Q13, R13, S13, T13, 
    A14, B14, C14, D14, E14, F14, G14, H14, I14, J14, K14, L14, M14, N14, O14, P14, Q14, R14, S14, T14, 
    A15, B15, C15, D15, E15, F15, G15, H15, I15, J15, K15, L15, M15, N15, O15, P15, Q15, R15, S15, T15, 
    A16, B16, C16, D16, E16, F16, G16, H16, I16, J16, K16, L16, M16, N16, O16, P16, Q16, R16, S16, T16, 
    A17, B17, C17, D17, E17, F17, G17, H17, I17, J17, K17, L17, M17, N17, O17, P17, Q17, R17, S17, T17, 
    A18, B18, C18, D18, E18, F18, G18, H18, I18, J18, K18, L18, M18, N18, O18, P18, Q18, R18, S18, T18, 
    A19, B19, C19, D19, E19, F19, G19, H19, I19, J19, K19, L19, M19, N19, O19, P19, Q19, R19, S19, T19, 
    A20, B20, C20, D20, E20, F20, G20, H20, I20, J20, K20, L20, M20, N20, O20, P20, Q20, R20, S20, T20
] = range(400) 

TILE_NAMES = [
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1", "j1", "k1", "l1", "m1", "n1", "o1", "p1", "q1", "r1", "s1", "t1", 
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "i2", "j2", "k2", "l2", "m2", "n2", "o2", "p2", "q2", "r2", "s2", "t2", 
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "i3", "j3", "k3", "l3", "m3", "n3", "o3", "p3", "q3", "r3", "s3", "t3", 
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "i4", "j4", "k4", "l4", "m4", "n4", "o4", "p4", "q4", "r4", "s4", "t4", 
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "i5", "j5", "k5", "l5", "m5", "n5", "o5", "p5", "q5", "r5", "s5", "t5", 
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "i6", "j6", "k6", "l6", "m6", "n6", "o6", "p6", "q6", "r6", "s6", "t6", 
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "i7", "j7", "k7", "l7", "m7", "n7", "o7", "p7", "q7", "r7", "s7", "t7", 
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8", "i8", "j8", "k8", "l8", "m8", "n8", "o8", "p8", "q8", "r8", "s8", "t8", 
    "a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9", "j9", "k9", "l9", "m9", "n9", "o9", "p9", "q9", "r9", "s9", "t9", 
    "a10", "b10", "c10", "d10", "e10", "f10", "g10", "h10", "i10", "j10", "k10", "l10", "m10", "n10", "o10", "p10", "q10", "r10", "s10", "t10", 
    "a11", "b11", "c11", "d11", "e11", "f11", "g11", "h11", "i11", "j11", "k11", "l11", "m11", "n11", "o11", "p11", "q11", "r11", "s11", "t11", 
    "a12", "b12", "c12", "d12", "e12", "f12", "g12", "h12", "i12", "j12", "k12", "l12", "m12", "n12", "o12", "p12", "q12", "r12", "s12", "t12", 
    "a13", "b13", "c13", "d13", "e13", "f13", "g13", "h13", "i13", "j13", "k13", "l13", "m13", "n13", "o13", "p13", "q13", "r13", "s13", "t13", 
    "a14", "b14", "c14", "d14", "e14", "f14", "g14", "h14", "i14", "j14", "k14", "l14", "m14", "n14", "o14", "p14", "q14", "r14", "s14", "t14", 
    "a15", "b15", "c15", "d15", "e15", "f15", "g15", "h15", "i15", "j15", "k15", "l15", "m15", "n15", "o15", "p15", "q15", "r15", "s15", "t15", 
    "a16", "b16", "c16", "d16", "e16", "f16", "g16", "h16", "i16", "j16", "k16", "l16", "m16", "n16", "o16", "p16", "q16", "r16", "s16", "t16", 
    "a17", "b17", "c17", "d17", "e17", "f17", "g17", "h17", "i17", "j17", "k17", "l17", "m17", "n17", "o17", "p17", "q17", "r17", "s17", "t17", 
    "a18", "b18", "c18", "d18", "e18", "f18", "g18", "h18", "i18", "j18", "k18", "l18", "m18", "n18", "o18", "p18", "q18", "r18", "s18", "t18", 
    "a19", "b19", "c19", "d19", "e19", "f19", "g19", "h19", "i19", "j19", "k19", "l19", "m19", "n19", "o19", "p19", "q19", "r19", "s19", "t19", 
    "a20", "b20", "c20", "d20", "e20", "f20", "g20", "h20", "i20", "j20", "k20", "l20", "m20", "n20", "o20", "p20", "q20", "r20", "s20", "t20"
]

def tile_to_coords(tile: Tile) -> tuple[int, int]: 
    """
    Returns y,x coordinates between 0 and 19 using bottom left as the origin.
    """
    return tile // 20, tile % 20

def coords_to_tile(y: int, x: int) -> Tile: 
    return y * 20 + x

Color = int
COLORS = [
    BLUE, YELLOW, RED, GREEN
] = range(4)

COLOR_NAMES = [
    'blue', 'yellow', 'red', 'green'
]

Rotation = int
ROTATIONS = [
    NORTH, EAST, SOUTH, WEST, NORTH_F, EAST_F, SOUTH_F, WEST_F
] = range(8)

ROTATION_NAMES = [
    'n', 'e', 's', 'w', 'nf', 'ef', 'sf', 'wf'
]

class _Piece: 

    def __init__(self, shape: np.array): 
        self.shapes, self.unique = _Piece.generate_rotations(shape) 
        self.contacts = _Piece.generate_contacts(self.shapes) 

        self.score = self.shapes[0].sum()

    @staticmethod
    def generate_rotations(shape: np.ndarray) -> tuple[list[np.ndarray], list[bool]]: 
        """
        Returns all possible flips and rotations of a base piece shape. 
        """
        out, unique = [], [] 

        def add(arr): 
            found = False 
            for x in out: 
                if x.shape == arr.shape and np.all(x == arr): 
                    found = True 
                    break 
            unique.append(not found) 
            out.append(arr) 

        # original shape, north
        cur = np.array(shape, dtype=np.uint8)[::-1] 
        add(cur) 

        # east
        cur = np.rot90(cur, 1) 
        add(cur)

        # south
        cur = np.rot90(cur, 1) 
        add(cur)

        # west
        cur = np.rot90(cur, 1) 
        add(cur)

        # flipped 
        n_unflipped = len(out) 
        for i in range(n_unflipped): 
            add(np.fliplr(out[i])) 

        return out, unique

    @staticmethod 
    def generate_contacts(shapes: list[np.ndarray]) -> list[np.ndarray]: 
        """
        Returns a list of tuples describing index and y,x coordinates of tiles 
        in a list of piece orientations that can be used to connect the piece 
        to an open corner on the board. 
        """
        out = [] 

        for shape in shapes: 
            contacts = np.zeros_like(shape, dtype=np.uint8)
            out.append(contacts) 

            H,W = shape.shape
            for y in range(H): 
                for x in range(W): 
                    # check each tile in piece 
                    if shape[y,x] != 0: 
                        v_neighbors = 0
                        h_neighbors = 0

                        if y > 0   and shape[y-1,x] != 0: v_neighbors += 1
                        if y < H-1 and shape[y+1,x] != 0: v_neighbors += 1
                        if x > 0   and shape[y,x-1] != 0: h_neighbors += 1
                        if x < W-1 and shape[y,x+1] != 0: h_neighbors += 1

                        n_neighbors = v_neighbors + h_neighbors

                        if (n_neighbors <= 1) or (v_neighbors == 1 and h_neighbors == 1): 
                            contacts[y, x] = 1
                    
        return out 
    
    def get_shape(self, rotation: Rotation) -> np.ndarray: 
        return self.shapes[rotation]
    
    def get_contacts(self, rotation: Rotation) -> np.ndarray: 
        return self.contacts[rotation]

PIECE_O1 = _Piece([[1]]) 

PIECE_I2 = _Piece([
    [1], 
    [1]
])

PIECE_I3 = _Piece([
    [1],
    [1],
    [1]
])
PIECE_L3 = _Piece([
    [1, 0], 
    [1, 1]
])

PIECE_I4 = _Piece([
    [1], 
    [1], 
    [1], 
    [1]
])
PIECE_L4 = _Piece([
    [1, 0], 
    [1, 0], 
    [1, 1]
])
PIECE_Z4 = _Piece([
    [1, 1, 0], 
    [0, 1, 1]
])
PIECE_O4 = _Piece([
    [1, 1], 
    [1, 1]
])
PIECE_T4 = _Piece([
    [1, 1, 1], 
    [0, 1, 0]
])

PIECE_F5 = _Piece([
    [0, 1, 1], 
    [1, 1, 0], 
    [0, 1, 0]
])
PIECE_I5 = _Piece([
    [1], 
    [1], 
    [1], 
    [1], 
    [1]
])
PIECE_L5 = _Piece([
    [1, 0], 
    [1, 0], 
    [1, 0], 
    [1, 1]
])
PIECE_N5 = _Piece([
    [0, 1], 
    [1, 1], 
    [1, 0], 
    [1, 0]
])
PIECE_P5 = _Piece([
    [1, 1], 
    [1, 1], 
    [1, 0]
])
PIECE_T5 = _Piece([
    [1, 1, 1], 
    [0, 1, 0], 
    [0, 1, 0]
])
PIECE_U5 = _Piece([
    [1, 0, 1], 
    [1, 1, 1]
])
PIECE_V5 = _Piece([
    [0, 0, 1], 
    [0, 0, 1], 
    [1, 1, 1]
])
PIECE_W5 = _Piece([
    [0, 0, 1], 
    [0, 1, 1], 
    [1, 1, 0]
])
PIECE_X5 = _Piece([
    [0, 1, 0], 
    [1, 1, 1], 
    [0, 1, 0]
])
PIECE_Y5 = _Piece([
    [0, 1], 
    [1, 1], 
    [0, 1], 
    [0, 1]
])
PIECE_Z5 = _Piece([
    [1, 1, 0], 
    [0, 1, 0], 
    [0, 1, 1]
])

PIECES = [
    PIECE_O1, PIECE_I2, PIECE_L3, PIECE_I3, PIECE_I4, PIECE_L4, PIECE_Z4, PIECE_O4, PIECE_T4, 
    PIECE_F5, PIECE_I5, PIECE_L5, PIECE_N5, PIECE_P5, PIECE_T5, PIECE_U5, PIECE_V5, PIECE_W5, 
    PIECE_X5, PIECE_Y5, PIECE_Z5
]

class Move: 

    def __init__(self, piece: PieceType, rotation: Rotation, contact: Tile, coord: Tile): 
        self.piece = piece 
        self.rotation = rotation
        self.contact = contact 
        self.coord = coord

    def __str__(self): 
        return f"{PIECE_NAMES[self.piece]}{ROTATION_NAMES[self.rotation]}-{TILE_NAMES[self.contact]}{TILE_NAMES[self.coord]}"

class _Player: 

    def __init__(self): 
        self.pieces = [True for _ in PIECE_TYPES]
        self.n_pieces = len(PIECE_TYPES) 
        self.score = 0
        self.legal = np.ones((400), dtype=np.uint8)
        self.corners = np.zeros((400), dtype=np.uint8)
        self.can_play = True 
        self.has_played = False

class _BoardState: 

    def __init__(self, n_players): 
        self.board = np.zeros((400), dtype=np.uint8)
        self.players = [_Player() for _ in range(n_players)] 
        self.turn = COLORS[0]
        self.ply = 0
        self.moves = [] 
        self.finished = False

        self.open_corners = np.zeros((400), dtype=np.uint8)
        self.open_corners[A01] = 1 
        self.open_corners[A20] = 1 
        self.open_corners[T01] = 1 
        self.open_corners[T20] = 1

    @property
    def winners(self): 
        if not self.finished: 
            return None 
        
        best = [0]
        for i in range(1, len(self.players)): 
            if self.players[i].score == self.players[best[0]].score: 
                best.append(i)
            elif self.players[i].score > self.players[best[0]].score: 
                best = [i]
        return best 

    def push_move(self, move: Move): 
        # remove tile 
        player = self.players[self.turn] 
        player.pieces[move.piece] = False 
        player.n_pieces -= 1 

        # add score 
        player.score += PIECES[move.piece].score

        # add piece to board 
        board = self.board.reshape((20, 20)) 
        shape = PIECES[move.piece].get_shape(move.rotation) 
        sy, sx = shape.shape
        y, x = tile_to_coords(move.coord) 
        cy, cx = tile_to_coords(move.contact) 
        y -= cy 
        x -= cx 
        board[y:y+sy,x:x+sx] += shape * (self.turn + 1)
        player.has_played = True 

        # remove corner from other players' starting position
        self.open_corners[move.coord] = 0 

        # find openings for each player 
        empty = (board == 0).astype(np.uint8)
        for p in range(len(self.players)): 
            pl = self.players[p] 
            if not pl.can_play: 
                continue 

            has_p = (board == p + 1).astype(np.uint8)

            legal = np.copy(empty) 
            legal[1:,:] &= ~has_p[:19,:]
            legal[:19,:] &= ~has_p[1:,:]
            legal[:,1:] &= ~has_p[:,:19]
            legal[:,:19] &= ~has_p[:,1:]

            corners = np.zeros_like(empty)
            corners[1:,1:] |= has_p[:19,:19]
            corners[1:,:19] |= has_p[:19,1:] 
            corners[:19,1:] |= has_p[1:,:19]
            corners[:19,:19] |= has_p[1:,1:]
            corners &= legal

            pl.legal[:] = legal.reshape(-1)
            pl.corners[:] = corners.reshape(-1)
            pl.can_play = len(self.get_legal_moves(unique=True, for_player=p)) > 0 

        # inc turn and make sure player can move 
        self.ply += 1
        cur_turn = self.turn
        while True: 
            self.turn += 1
            if self.turn >= len(self.players): 
                self.turn = 0 
            if self.players[self.turn].can_play: 
                break 

            # looped all the way back to same player 
            # no player can play, game is done
            if cur_turn == self.turn: 
                self.finished = True 
                break 

    def is_legal(self, move: Move, for_player: int=None): 
        # no move is legal after game is done 
        if self.finished: 
            return False 
        
        if for_player is None: 
            for_player = self.turn

        # player must not have played the piece yet 
        player = self.players[for_player] 
        if not player.pieces[move.piece]: 
            return False 

        diags = player.corners

        # first move must be in a corner 
        if not player.has_played: 
            diags = self.open_corners 

        # piece must be placed on a diagonal (or corner on first move) 
        if diags[move.coord] != 1: 
            return False
        
        pc = PIECES[move.piece] 
        shape = pc.get_shape(move.rotation) 
        contacts = pc.get_contacts(move.rotation) 

        # contact tile must be an endpoint or corner of the piece 
        cy, cx = tile_to_coords(move.contact) 
        sy, sx = contacts.shape
        if cy >= sy or cx >= sx or contacts[cy,cx] == 0: 
            return False
        
        # piece must be placed in bounds 
        dn = sy - cy - 1 
        ds = cy 
        de = sx - cx - 1 
        dw = cx 
        y, x = tile_to_coords(move.coord) 
        if y + dn >= 20: return False
        if y - ds < 0: return False
        if x + de >= 20: return False
        if x - dw < 0: return False

        # tiles must not overlap 
        y -= cy 
        x -= cx 
        if np.any((self.board.reshape((20, 20))[y:y+sy,x:x+sx] != 0) & shape): 
            return False
        
        # no part of the piece may be adjacent to the player's other pieces
        if np.any((player.legal.reshape((20, 20))[y:y+sy,x:x+sx] & shape) != shape): 
            return False
        
        return True 
    
    def get_pseudolegal_moves(self, unique=False, for_player: int=None) -> list[Move]: 
        if self.finished: 
            return []
        
        out = [] 

        if for_player is None: 
            for_player = self.turn

        player = self.players[for_player] 
        diags = player.corners
        if not player.can_play: 
            return [] 

        # first move must be in a corner 
        if not player.has_played: 
            diags = self.open_corners 

        for diag in diags.nonzero()[0]: 
            for pc, has in enumerate(player.pieces): 
                if has: 
                    rotations = PIECES[pc].contacts 
                    for rot, contacts in enumerate(rotations): 
                        if unique and not PIECES[pc].unique[rot]: 
                            continue 
                        for y, x in zip(*contacts.nonzero()): 
                            out.append(Move(pc, rot, coords_to_tile(y, x), diag))

        return out 
    
    def get_legal_moves(self, unique=False, for_player=None) -> list[Move]: 
        pseudo = self.get_pseudolegal_moves(unique=unique, for_player=for_player) 

        out = [] 
        for mv in pseudo: 
            if self.is_legal(mv, for_player=for_player): 
                out.append(mv)
        
        return out 
    
    def __str__(self): 
        out = "" 
        
        board = self.board.reshape((20, 20))[::-1]
        chars = [
            '.', 
            '\033[94mB\033[0m', 
            '\033[93mY\033[0m', 
            '\033[91mR\033[0m', 
            '\033[92mG\033[0m'
        ]

        for y in range(20): 
            for x in range(20): 
                out += f"{chars[board[y,x]]} "
            out += "\n"

        for i in range(len(self.players)): 
            out += f"{chars[i+1]}: {int(self.players[i].score)} "
            if sum(int(x) for x in self.players[i].pieces) > 0: 
                out += "( "
                for pc, has in enumerate(self.players[i].pieces): 
                    if has: 
                        out += PIECE_NAMES[pc] + " "
                out += ")\n"

        out += f"Finished: {self.finished}"
        if self.finished: 
            out += f"\nWinner: "
            for p in self.winners: 
                out += f"{chars[p+1]} "
        else: 
            out += f"\nTurn: {chars[self.turn+1]}"

        return out 

class Board: 

    def __init__(self, n_players: int): 
        self.stack = [_BoardState(n_players=n_players)]
    
    @property
    def state(self): 
        return self.stack[-1]
    
    @property 
    def finished(self): 
        return self.state.finished 

    @property 
    def winners(self): 
        return self.state.winners

    def get_pseudolegal_moves(self, unique=False) -> list[Move]: 
        return self.state.get_pseudolegal_moves(unique=unique) 

    def get_legal_moves(self, unique=False) -> list[Move]: 
        return self.state.get_legal_moves(unique=unique) 

    def is_legal(self, move: Move) -> bool: 
        return self.state.is_legal(move) 

    def push_move(self, move: Move): 
        """
        Plays a move on the board. The move is assumed to be legal (it can be
        checked with `Board.is_legal()`).
        """
        board = copy.deepcopy(self.state) 
        board.push_move(move) 
        self.stack.append(board) 
        
    def pop_move(self): 
        self.stack.pop() 

    def __str__(self): 
        return str(self.state)
