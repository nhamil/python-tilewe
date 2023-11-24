#define PY_SSIZE_T_CLEAN
#include <Python.h> 

#include <stdlib.h> 

#include "Tilewe/Tilewe.h" 

typedef struct MoveObject MoveObject; 

struct MoveObject 
{
    PyObject_HEAD 
    Tw_Move Move; 
};

static int Move_init(MoveObject* self, PyObject* args, PyObject* kwds) 
{
    static const char* kwlist[] = 
    {
        "piece", 
        "rotation", 
        "contact", 
        "to_tile", 
        NULL
    };

    unsigned pc, rot, con, tile; 
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "IIII", kwlist, &pc, &rot, &con, &tile)) 
    {
        PyErr_SetString(PyExc_AttributeError, "all parameters must be used"); 
        return false;
    }

    self->Move = Tw_MakeMove_Safe(pc, rot, con, tile); 

    if (self->Move == Tw_NoMove) 
    {
        PyErr_SetString(PyExc_AttributeError, "move must have a valid piece, rotation, contact, and tile combination"); 
        return -1; 
    }

    return 0; 
}

static PyObject* Move_str(MoveObject* self, PyObject* Py_UNUSED(ignored)) 
{
    char buf[32]; 
    snprintf(buf, 32, "%s%s-%s%s", 
        Tw_Pc_Str(Tw_Move_Pc(self->Move)), 
        Tw_Rot_Str(Tw_Move_Rot(self->Move)), 
        Tw_Tile_Str(Tw_Move_Con(self->Move)), 
        Tw_Tile_Str(Tw_Move_ToTile(self->Move))
    );

    return PyUnicode_FromString(buf); 
}

static PyObject* Move_Piece(MoveObject* self, void* closure) 
{
    return PyLong_FromLong(Tw_Move_Pc(self->Move)); 
}

static PyObject* Move_Rotation(MoveObject* self, void* closure) 
{
    return PyLong_FromLong(Tw_Move_Rot(self->Move)); 
}

static PyObject* Move_Contact(MoveObject* self, void* closure) 
{
    return PyLong_FromLong(Tw_Move_Con(self->Move)); 
}

static PyObject* Move_Tile(MoveObject* self, void* closure) 
{
    return PyLong_FromLong(Tw_Move_ToTile(self->Move)); 
}

static PyGetSetDef Move_getsets[] = 
{
    { "piece", Move_Piece, NULL, "Gets the move piece", NULL },
    { "rotation", Move_Rotation, NULL, "Gets the move rotation", NULL },
    { "contact", Move_Contact, NULL, "Gets the move contact tile", NULL },
    { "to_tile", Move_Tile, NULL, "Gets the move open corner", NULL },
    { NULL }
};

static PyTypeObject MoveType = 
{
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0) 
    .tp_name = "ctilewe.Move", 
    .tp_doc = PyDoc_STR("Representation of a Move."), 
    .tp_basicsize = sizeof(MoveObject), 
    .tp_itemsize = 0, 
    .tp_flags = Py_TPFLAGS_DEFAULT, 
    .tp_new = PyType_GenericNew, 
    .tp_init = Move_init, 
    .tp_str = Move_str, 
    .tp_repr = Move_str, 
    .tp_getset = Move_getsets
};

typedef struct BoardObject BoardObject; 

struct BoardObject 
{
    PyObject_HEAD 
    Tw_Board Board; 
};

static int Board_init(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    static const char* kwlist[] = { "n_players", NULL }; 

    int numPlayers = 4; 
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, &numPlayers)) 
    {
        return -1; 
    }

    if (numPlayers < 1 || numPlayers > 4) 
    {
        PyErr_SetString(PyExc_AttributeError, "n_players must be between 1 and 4"); 
        return -1; 
    }

    Tw_InitBoard(&self->Board, numPlayers); 
    return 0; 
}

static PyObject* Board_CurrentPlayer(BoardObject* self, void* closure) 
{
    return PyLong_FromLong(self->Board.CurTurn); 
}

static PyObject* Board_NumPlayers(BoardObject* self, void* closure) 
{
    return PyLong_FromLong(self->Board.NumPlayers); 
}

static PyObject* Board_Finished(BoardObject* self, void* closure) 
{
    return PyBool_FromLong(self->Board.Finished); 
}

static PyObject* Board_Ply(BoardObject* self, void* closure) 
{
    return PyLong_FromLong(self->Board.Ply); 
}

static PyObject* Board_Moves(BoardObject* self, void* closure) 
{
    PyObject* list = PyList_New((unsigned) self->Board.Ply); 

    for (int i = 0; i < self->Board.Ply; i++) 
    {
        PyList_SetItem(
            list, 
            i, 
            PyLong_FromUnsignedLong(self->Board.History[i].Move)
        );
    }

    return list; 
}

static PyObject* Board_Scores(BoardObject* self, void* closure) 
{
    PyObject* list = PyList_New((unsigned) self->Board.NumPlayers); 

    for (int i = 0; i < self->Board.NumPlayers; i++) 
    {
        PyList_SetItem(
            list, 
            i, 
            PyLong_FromLong(self->Board.Players[i].Score)
        );
    }

    return list; 
}

static PyObject* Board_Winners(BoardObject* self, void* closure) 
{
    PyObject* list = PyList_New(0); 

    int best = -1; 
    for (int i = 0; i < self->Board.NumPlayers; i++) 
    {
        int score = self->Board.Players[i].Score; 

        if (score > best) 
        {
            PyList_SetSlice(list, 0, PyList_Size(list), NULL); 
            best = score; 
        }

        if (score == best) 
        {
            PyList_Append(list, PyLong_FromLong(i)); 
        }
    }

    return list; 
}

static PyObject* Board_GenMoves(BoardObject* self, PyObject* Py_UNUSED(ignored)) 
{
    Tw_MoveList moves; 
    Tw_InitMoveList(&moves); 
    Tw_Board_GenMoves(&self->Board, &moves); 

    PyObject* list = PyList_New(moves.Count); 

    for (int i = 0; i < moves.Count; i++) 
    {
        MoveObject* mv = PyObject_New(MoveObject, &MoveType); 
        mv->Move = moves.Elements[i]; 

        PyList_SetItem(list, i, mv); 
    }

    return list; 
}

static PyObject* Board_Push(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    static const char* kwlist[] = 
    {
        "move", 
        NULL
    };

    MoveObject* move; 

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, &move)) 
    {
        return NULL; 
    }

    if (!PyObject_TypeCheck(move, &MoveType)) 
    {
        PyErr_SetString(PyExc_AttributeError, "Must be a move"); 
        return NULL; 
    }

    Tw_Board_Push(&self->Board, move->Move); 

    Py_RETURN_NONE; 
}

static PyObject* Board_ColorAt(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    static const char* kwlist[] = 
    {
        "tile", 
        NULL
    };

    unsigned long tile; 

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "I", kwlist, &tile)) 
    {
        return NULL; 
    }

    return PyLong_FromUnsignedLong(Tw_Board_ColorAt(&self->Board, tile)); 
}

static bool ForPlayerArgHandler(BoardObject* self, PyObject* args, PyObject* kwds, int* player) 
{
    static const char* kwlist[] = 
    {
        "for_player", 
        NULL
    };

    *player = Tw_Color_None; 

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, player)) 
    {
        *player = -1; 
        return false;
    }

    if (*player == Tw_Color_None) 
    {
        *player = self->Board.CurTurn; 
    }

    if (*player < 0 || *player >= self->Board.NumPlayers) 
    {
        *player = -1; 
        PyErr_SetString(PyExc_AttributeError, "for_player must be valid or None"); 
        return false;
    }

    return true;
}

// TODO use better way that doesn't duplicate so much code 
static bool ForPlayerAndMoveArgHandler(BoardObject* self, PyObject* args, PyObject* kwds, Tw_Move* move, int* player) 
{
    static const char* kwlist[] = 
    {
        "move", 
        "for_player", 
        NULL
    };

    MoveObject* moveObj; 
    *player = Tw_Color_None; 

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|i", kwlist, &moveObj, player)) 
    {
        *move = (unsigned) Tw_NoMove; 
        *player = -1; 
        return false;
    }

    if (!PyObject_TypeCheck(moveObj, &MoveType)) 
    {
        PyErr_SetString(PyExc_AttributeError, "Must be a move"); 
        return false; 
    }

    *move = moveObj->Move; 

    if (*player == Tw_Color_None) 
    {
        *player = self->Board.CurTurn; 
    }

    if (*player < 0 || *player >= self->Board.NumPlayers) 
    {
        *move = (unsigned) Tw_NoMove; 
        *player = -1; 
        PyErr_SetString(PyExc_AttributeError, "for_player must be valid or None"); 
        return false;
    }

    return true;
}

static PyObject* Board_NumLegalMoves(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_Board_NumMovesForPlayer(&self->Board, (Tw_Color) player)); 
}

static PyObject* Board_PlayerPcs(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    // get a list of the player's pieces
    Tw_PcList pcs;
    Tw_InitPcList(&pcs);
    Tw_Board_PlayerPcs(&self->Board, player, &pcs);

    // build Python list of the pieces
    PyObject* list = PyList_New(pcs.Count); 
    for (int i = 0; i < pcs.Count; i++) {
        PyList_SetItem(
            list, 
            i, 
            PyLong_FromUnsignedLong((unsigned long) pcs.Elements[i])
        ); 
    }

    return list; 
}

static PyObject* Board_NumPlayerPcs(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_Board_NumPlayerPcs(&self->Board, (Tw_Color) player)); 
}

static PyObject* Board_PlayerCorners(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    // get a list of the player's open corners
    Tw_TileList openCorners;
    Tw_InitTileList(&openCorners);
    Tw_Board_PlayerCorners(&self->Board, player, &openCorners);

    // build Python list of the open corner tiles
    PyObject* list = PyList_New(openCorners.Count); 
    for (int i = 0; i < openCorners.Count; i++) {
        PyList_SetItem(
            list, 
            i, 
            PyLong_FromUnsignedLong((unsigned long) openCorners.Elements[i])
        ); 
    }

    return list; 
}

static PyObject* Board_PlayerScore(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    return PyLong_FromLong(self->Board.Players[player].Score); 
}

static PyObject* Board_CanPlay(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    return PyBool_FromLong((long) self->Board.Players[player].CanPlay); 
}

static PyObject* Board_NumPlayerCorners(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_Board_NumPlayerCorners(&self->Board, player)); 
}

static PyObject* Board_IsLegal(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    Tw_Move move; 
    if (!ForPlayerAndMoveArgHandler(self, args, kwds, &move, &player))
    {
        return NULL;
    }

    return PyBool_FromLong(Tw_Board_IsLegalForPlayer(&self->Board, (Tw_Color) player, move)); 
}

static PyObject* Board_Pop(BoardObject* self, PyObject* Py_UNUSED(ignored)) 
{
    Tw_Board_Pop(&self->Board); 
    Py_RETURN_NONE; 
}

static PyObject* Board_str(BoardObject* self, PyObject* Py_UNUSED(ignored)) 
{
    char buf[Tw_BoardStrSize]; 
    Tw_Board_ToStr(&self->Board, buf); 

    return PyUnicode_FromString(buf); 
}

static PyGetSetDef Board_getsets[] = 
{
    { "moves", Board_Moves, NULL, "Move history", NULL },
    { "finished", Board_Finished, NULL, "Whether the game is done", NULL },
    { "n_players", Board_NumPlayers, NULL, "Number of players", NULL },
    { "current_player", Board_CurrentPlayer, NULL, "Color of the current player", NULL },
    { "cur_player", Board_CurrentPlayer, NULL, "Color of the current player", NULL },
    { "ply", Board_Ply, NULL, "Current board ply", NULL },
    { "scores", Board_Scores, NULL, "Scores of all players", NULL },
    { "winners", Board_Winners, NULL, "Gets list of player indices who have the highest score", NULL },
    { NULL }
};

static PyMethodDef Board_methods[] = 
{
    { "generate_legal_moves", Board_GenMoves, METH_VARARGS | METH_KEYWORDS, "Returns a list of legal moves" }, 
    { "gen_moves", Board_GenMoves, METH_VARARGS | METH_KEYWORDS, "Returns a list of legal moves" }, 
    { "push", Board_Push, METH_VARARGS | METH_KEYWORDS, "Plays a move" }, 
    { "pop", Board_Pop, METH_NOARGS, "Undoes a move" }, 
    { "color_at", Board_ColorAt, METH_VARARGS | METH_KEYWORDS, "Color that claimed the tile" }, 
    { "n_legal_moves", Board_NumLegalMoves, METH_VARARGS | METH_KEYWORDS, "Gets total number of legal moves for a player" }, 
    { "n_remaining_pieces", Board_NumPlayerPcs, METH_VARARGS | METH_KEYWORDS, "Gets total number of pieces remaining for a player" }, 
    { "remaining_pieces", Board_PlayerPcs, METH_VARARGS | METH_KEYWORDS, "Gets a list of pieces remaining for a player" }, 
    { "n_player_corners", Board_NumPlayerCorners, METH_VARARGS | METH_KEYWORDS, "Gets total number of open corners for a player" }, 
    { "player_corners", Board_PlayerCorners, METH_VARARGS | METH_KEYWORDS, "Gets a list of the open corners for a player" }, 
    { "player_score", Board_PlayerScore, METH_VARARGS | METH_KEYWORDS, "Gets the score of a player" }, 
    { "can_play", Board_CanPlay, METH_VARARGS | METH_KEYWORDS, "Whether a player has remaining moves" }, 
    { "is_legal", Board_IsLegal, METH_VARARGS | METH_KEYWORDS, "Whether a move is legal for a player" }, 
    // { "copy", Board_Copy, METH_NOARGS, "Returns a clone of the current board state" }, 
    { NULL }
};

static PyTypeObject BoardType = 
{
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0) 
    .tp_name = "ctilewe.Board", 
    .tp_doc = PyDoc_STR("Public representation of a game Board which is how players or bots interface with the game."), 
    .tp_basicsize = sizeof(BoardObject), 
    .tp_itemsize = 0, 
    .tp_flags = Py_TPFLAGS_DEFAULT, 
    .tp_new = PyType_GenericNew, 
    .tp_init = Board_init, 
    .tp_str = Board_str, 
    .tp_getset = Board_getsets, 
    .tp_methods = Board_methods
};

static bool TileArgHandler(PyObject* args, PyObject* kwds, bool checkBounds, Tw_Tile* tile) 
{
    static const char* kwlist[] = 
    {
        "tile", 
        NULL
    };

    *tile = Tw_Tile_None; 

    unsigned tileValue; 
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "I", kwlist, &tileValue)) 
    {
        return false;
    }

    *tile = (Tw_Tile) tileValue; 

    if (checkBounds && !Tw_Tile_InBounds(*tile)) 
    {
        PyErr_SetString(PyExc_AttributeError, "tile must be in bounds"); 
        return false;
    }

    return true;
}

static bool CoordsArgHandler(PyObject* args, PyObject* kwds, bool checkBounds, int vals[2]) 
{
    static const char* kwlist[] = 
    {
        "coords", 
        NULL
    };

    vals[0] = vals[1] = 0; 

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "(ii)", kwlist, vals, vals + 1)) 
    {
        return false;
    }

    if (checkBounds && !Tw_CoordsInBounds(vals[0], vals[1])) 
    {
        PyErr_SetString(PyExc_AttributeError, "coords must be in bounds"); 
        return false;
    }

    return true;
}

static bool PcArgHandler(PyObject* args, PyObject* kwds, bool checkBounds, Tw_Pc* pc) 
{
    static const char* kwlist[] = 
    {
        "piece", 
        NULL
    };

    *pc = Tw_Pc_None; 

    unsigned pcValue; 
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "I", kwlist, &pcValue)) 
    {
        return false;
    }

    *pc = (Tw_Pc) pcValue; 

    if (checkBounds && !Tw_Tile_InBounds(*pc)) 
    {
        PyErr_SetString(PyExc_AttributeError, "piece must be valid"); 
        return false;
    }

    return true;
}

static bool PcRotArgHandler(PyObject* args, PyObject* kwds, bool checkBounds, Tw_Pc* pc, Tw_Rot* rot) 
{
    static const char* kwlist[] = 
    {
        "piece", 
        "rotation", 
        NULL
    };

    *pc = Tw_Pc_None; 
    *rot = Tw_Rot_N; 

    unsigned pcValue, rotValue; 
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "II", kwlist, &pcValue, &rotValue)) 
    {
        return false;
    }

    *pc = (Tw_Pc) pcValue; 
    *rot = (Tw_Rot) rotValue; 

    if (checkBounds && !Tw_Tile_InBounds(*pc)) 
    {
        PyErr_SetString(PyExc_AttributeError, "piece must be valid"); 
        return false;
    }

    if (checkBounds && (*rot < 0 || *rot >= Tw_NumRots))
    {
        PyErr_SetString(PyExc_AttributeError, "rotation must be valid"); 
        return false;
    }

    return true;
}

static bool MoveArgHandler(PyObject* args, PyObject* kwds, bool checkBounds, Tw_Move* move) 
{
    static const char* kwlist[] = 
    {
        "move", 
        NULL
    };

    *move = Tw_NoMove; 

    unsigned moveValue; 
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "I", kwlist, &moveValue)) 
    {
        return false;
    }

    Tw_Move tmp = *move = (Tw_Move) moveValue; 

    if (checkBounds && (tmp == Tw_NoMove || tmp != Tw_MakeMove_Safe(
        Tw_Move_Pc(tmp), 
        Tw_Move_Rot(tmp), 
        Tw_Move_Con(tmp), 
        Tw_Move_ToTile(tmp) 
    ))) 
    {
        PyErr_SetString(PyExc_AttributeError, "move must be valid"); 
        return false;
    }

    return true;
}

static PyObject* Tilewe_TileToCoords(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Tile tile; 
    if (!TileArgHandler(args, kwds, true, &tile)) 
    {
        return NULL;
    }

    int x, y; 
    Tw_Tile_ToCoords(tile, &x, &y); 

    return Py_BuildValue("ii", x, y); 
}

static PyObject* Tilewe_TileInBounds(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Tile tile; 
    if (!TileArgHandler(args, kwds, false, &tile)) 
    {
        return NULL;
    }

    return PyBool_FromLong(Tw_Tile_InBounds(tile)); 
}

static PyObject* Tilewe_CoordsToTile(PyObject* self, PyObject* args, PyObject* kwds) 
{
    int vals[2]; 
    if (!CoordsArgHandler(args, kwds, true, vals)) 
    {
        return NULL;
    }

    return Py_BuildValue("i", Tw_MakeTile(vals[0], vals[1])); 
}

static PyObject* Tilewe_CoordsInBounds(PyObject* self, PyObject* args, PyObject* kwds) 
{
    int vals[2]; 
    if (!CoordsArgHandler(args, kwds, false, vals)) 
    {
        return NULL;
    }

    return PyBool_FromLong(Tw_CoordsInBounds(vals[0], vals[1])); 
}

static PyObject* Tilewe_NumPcContacts(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Pc pc; 
    if (!PcArgHandler(args, kwds, true, &pc)) 
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_TileSet_Count(&Tw_RotPcInfos[Tw_ToRotPc(pc, Tw_Rot_N)].Contacts)); 
}

static PyObject* Tilewe_NumPcTiles(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Pc pc; 
    if (!PcArgHandler(args, kwds, true, &pc)) 
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_TileSet_Count(&Tw_RotPcInfos[Tw_ToRotPc(pc, Tw_Rot_N)].Tiles)); 
}

static PyObject* Tilewe_NumPcCorners(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Pc pc; 
    if (!PcArgHandler(args, kwds, true, &pc)) 
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_TileSet_Count(&Tw_RotPcInfos[Tw_ToRotPc(pc, Tw_Rot_N)].RelCorners)); 
}

static PyObject* Tilewe_PcTiles(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Pc pc; 
    Tw_Rot rot; 
    if (!PcRotArgHandler(args, kwds, true, &pc, &rot)) 
    {
        return NULL;
    }

    PyObject* list = PyList_New(0); 

    Tw_TileSet_FOR_EACH(Tw_RotPcInfos[Tw_ToRotPc(pc, rot)].Tiles, tile, 
    {
        PyList_Append(list, PyLong_FromLong((long) tile)); 
    });

    return list; 
}

static PyObject* Tilewe_PcContacts(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Pc pc; 
    Tw_Rot rot; 
    if (!PcRotArgHandler(args, kwds, true, &pc, &rot)) 
    {
        return NULL;
    }

    PyObject* list = PyList_New(0); 

    Tw_TileSet_FOR_EACH(Tw_RotPcInfos[Tw_ToRotPc(pc, Tw_Rot_N)].Contacts, tile, 
    {
        PyList_Append(list, PyLong_FromLong((long) tile)); 
    });

    return list; 
}

static PyObject* Tilewe_MovePc(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Move move; 
    if (!MoveArgHandler(args, kwds, true, &move)) 
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_Move_Pc(move)); 
}

static PyObject* Tilewe_MoveRot(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Move move; 
    if (!MoveArgHandler(args, kwds, true, &move)) 
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_Move_Rot(move)); 
}


static PyObject* Tilewe_MoveCon(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Move move; 
    if (!MoveArgHandler(args, kwds, true, &move)) 
    {
        return NULL;
    }


    return PyLong_FromLong(Tw_Move_Con(move)); 
}

static PyObject* Tilewe_MoveTile(PyObject* self, PyObject* args, PyObject* kwds) 
{
    Tw_Move move; 
    if (!MoveArgHandler(args, kwds, true, &move)) 
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_Move_ToTile(move)); 
}

static PyObject* Tilewe_CreateMove(PyObject* self, PyObject* args, PyObject* kwds) 
{
    static const char* kwlist[] = 
    {
        "piece", 
        "rotation", 
        "contact", 
        "to_tile", 
        NULL
    };

    unsigned pc, rot, con, tile; 
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "IIII", kwlist, &pc, &rot, &con, &tile)) 
    {
        // PyErr_SetString(PyExc_AttributeError, "piece must be valid"); 
        return false;
    }

    Tw_Move move = Tw_MakeMove_Safe(pc, rot, con, tile); 

    if (move == Tw_NoMove) 
    {
        Py_RETURN_NONE; 
    }
    else 
    {
        PyLong_FromLong(move); 
    }
}

static PyObject* Tilewe_PlayRandomGame(PyObject* self, PyObject* args) 
{
    Tw_Board board[1]; 
    Tw_MoveList moves[1]; 
    Tw_InitBoard(board, 4); 

    while (!board->Finished) 
    {
        Tw_InitMoveList(moves); 
        Tw_Board_GenMoves(board, moves); 
        Tw_Board_Push(board, moves->Elements[rand() % moves->Count]); 
    }

    Tw_Board_Print(board); 

    Py_RETURN_NONE; 
}

static PyMethodDef TileweMethods[] = 
{
    { "play_random_game", Tilewe_PlayRandomGame, METH_NOARGS, "Plays a random game" }, 
    { "tile_to_coords", Tilewe_TileToCoords, METH_VARARGS | METH_KEYWORDS, "Get x,y coordinates of a tile" }, 
    { "tile_in_bounds", Tilewe_TileInBounds, METH_VARARGS | METH_KEYWORDS, "Checks if tile is in bounds" }, 
    { "coords_to_tile", Tilewe_CoordsToTile, METH_VARARGS | METH_KEYWORDS, "Get tile from x,y coordinates" }, 
    { "coords_in_bounds", Tilewe_CoordsInBounds, METH_VARARGS | METH_KEYWORDS, "Checks if coords are in bounds" }, 
    { "n_piece_tiles", Tilewe_NumPcTiles, METH_VARARGS | METH_KEYWORDS, "Gets number of tiles in a piece" }, 
    { "n_piece_contacts", Tilewe_NumPcContacts, METH_VARARGS | METH_KEYWORDS, "Gets number of contacts in a piece" }, 
    { "n_piece_corners", Tilewe_NumPcCorners, METH_VARARGS | METH_KEYWORDS, "Gets number of corners in a piece" }, 
    { "piece_tiles", Tilewe_PcTiles, METH_VARARGS | METH_KEYWORDS, "Gets tiles in a rotated piece" }, 
    { "piece_contacts", Tilewe_PcContacts, METH_VARARGS | METH_KEYWORDS, "Gets contacts in a rotated piece" }, 
    { NULL, NULL, 0, NULL }
};

static PyModuleDef TileweModule = 
{
    .m_base = PyModuleDef_HEAD_INIT, 
    .m_name = "ctilewe", 
    .m_doc = "Contains Tilewe implementation", 
    .m_size = -1, 
    .m_methods = TileweMethods
};

PyMODINIT_FUNC PyInit_ctilewe(void) 
{
    Tw_Init(); 

    PyObject* m; 

    if (PyType_Ready(&BoardType) < 0) return NULL; 
    if (PyType_Ready(&MoveType) < 0) return NULL; 

    if (!(m = PyModule_Create(&TileweModule))) return NULL; 

    Py_INCREF(&BoardType); 
    if (PyModule_AddObject(m, "Board", (PyObject*) &BoardType) < 0) 
    {
        Py_DECREF(&BoardType); 
        Py_DECREF(m); 
        return NULL; 
    }

    Py_INCREF(&MoveType); 
    if (PyModule_AddObject(m, "Move", (PyObject*) &MoveType) < 0) 
    {
        Py_DECREF(&MoveType); 
        Py_DECREF(m); 
        return NULL; 
    }

    return m; 
}
