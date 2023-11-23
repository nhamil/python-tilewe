#define PY_SSIZE_T_CLEAN
#include <Python.h> 

#include <stdlib.h> 

#include "Tilewe/Tilewe.h" 

typedef struct BoardObject BoardObject; 

struct BoardObject 
{
    PyObject_HEAD 
    Tw_Board Board; 
};

static int Board_init(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    static char* kwlist[] = { "n_players", NULL }; 

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
        PyList_SetItem(
            list, 
            i, 
            PyLong_FromUnsignedLong((unsigned long) moves.Elements[i])
        ); 
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

    unsigned long long move; 

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "L", kwlist, &move)) 
    {
        return NULL; 
    }

    Tw_Board_Push(&self->Board, (Tw_Move) move); 

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

static PyObject* Board_NumPlayerCorners(BoardObject* self, PyObject* args, PyObject* kwds) 
{
    int player;
    if (!ForPlayerArgHandler(self, args, kwds, &player))
    {
        return NULL;
    }

    return PyLong_FromLong(Tw_Board_NumPlayerCorners(&self->Board, player)); 
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
    { "generate_legal_moves", Board_GenMoves, METH_NOARGS, "Returns a list of legal moves" }, 
    { "gen_moves", Board_GenMoves, METH_NOARGS, "Returns a list of legal moves" }, 
    { "push", Board_Push, METH_VARARGS | METH_KEYWORDS, "Plays a move" }, 
    { "pop", Board_Pop, METH_NOARGS, "Undoes a move" }, 
    { "color_at", Board_ColorAt, METH_VARARGS | METH_KEYWORDS, "Color that claimed the tile" }, 
    { "n_legal_moves", Board_NumLegalMoves, METH_VARARGS | METH_KEYWORDS, "Gets total number of legal moves for a player" }, 
    { "n_remaining_pieces", Board_NumPlayerPcs, METH_VARARGS | METH_KEYWORDS, "Gets total number of pieces remaining for a player" }, 
    { "remaining_pieces", Board_PlayerPcs, METH_VARARGS | METH_KEYWORDS, "Gets a list of pieces remaining for a player" }, 
    { "n_player_corners", Board_NumPlayerCorners, METH_VARARGS | METH_KEYWORDS, "Gets total number of open corners for a player" }, 
    { "player_corners", Board_PlayerCorners, METH_VARARGS | METH_KEYWORDS, "Gets a list of the open corners for a player" }, 
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

static PyMethodDef TileweMethods[] = 
{
    { "play_random_game", Tilewe_PlayRandomGame, METH_NOARGS, "Plays a random game" }, 
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
    PyObject* m; 

    if (PyType_Ready(&BoardType) < 0) return NULL; 

    if (!(m = PyModule_Create(&TileweModule))) return NULL; 

    Py_INCREF(&BoardType); 
    if (PyModule_AddObject(m, "Board", (PyObject*) &BoardType) < 0) 
    {
        Py_DECREF(&BoardType); 
        Py_DECREF(m); 
        return NULL; 
    }

    return m; 
}
