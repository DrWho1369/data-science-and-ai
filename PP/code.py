import pytest
from chess_puzzle import *
import tempfile


# Testing location2index

def test_location2index1():
    assert location2index("e2") == (5,2)


def test_location2index2():
    assert location2index("E2") == (5,2)


def test_location2index3():
    assert location2index("a1") == (1,1)


def test_location2index4():
    assert location2index("z26") == (26,26)


def test_location2index5():
    assert location2index("m13") == (13,13)


# Testing index2location

def test_index2location1():
    assert index2location(5,2) == "e2"


def test_index2location2():
    assert index2location(1,1) == "a1"


def test_index2location3():
    assert index2location(26,26) == "z26"


def test_index2location4():
    assert index2location(2,26) == "b26"


def test_index2location5():
    assert index2location(26,2) == "z2"


# Initialising some set ups

wr1 = Rook(3,4,True)
wk1 = King(3,5,True)


br1 = Rook(3,1,False)
bk1 = King(2,3,False)


B1 = (5, [wr1, wk1, br1, bk1])


# Testing is_piece_at()

def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False


def test_is_piece_at2():
    assert is_piece_at(3,4,B1) == True


def test_is_piece_at3():
    assert is_piece_at(3,5,B1) == True


def test_is_piece_at4():
    assert is_piece_at(3,1,B1) == True


def test_is_piece_at5():
    assert is_piece_at(2,3,B1) == True


def test_is_piece_at6():
    assert is_piece_at(1,1,B1) == False


# Testing piece_at()

def test_piece_at1():
    assert piece_at(3,4, B1) == wr1


def test_piece_at2():
    assert piece_at(2,3,B1) == bk1


def test_piece_at3():
    assert piece_at(3,1,B1) == br1


def test_piece_at4():
    assert piece_at(3,5,B1) == wk1


def test_piece_at5():
    board = (5, [King(5, 5, True)])
    assert piece_at(5, 5, board).side == True


# Testing can_reach()

def test_can_reach1():
    assert wr1.can_reach(5,4, B1) == True


def test_can_reach2():
    assert wr1.can_reach(3,5,B1) == False


def test_can_reach3():
    assert wr1.can_reach(3,1,B1) == True


def test_can_reach4():
    assert wr1.can_reach(4, 5, B1) == False


def test_can_reach5():
    assert wr1.can_reach(1, 4, B1) == True


# Testing Can_move_to() for the rook class:

wr2 = Rook(2, 2, True)
wk2 = King(1, 1, True)
br2 = Rook(2, 5, False)
bk2 = King(5, 5, False)

test_board_2: Board = (6, [wr2, wk2, br2, bk2])


def test_can_move_to1():
    assert wr1.can_move_to(5,4, B1) == False


def test_can_move_to2():
    '''Purpose of test: check rook can make vertical move with
    a clear path'''
    assert wr2.can_move_to(2, 4, test_board_2) == True


def test_can_move_to3():
    '''Purpose of test: move is blocked by rooks own king'''
    assert wr2.can_move_to(1, 1, test_board_2) == False


def test_can_move_to4():
    '''Purpose of test: check if rook can capture opposites side rook'''
    assert wr2.can_move_to(2, 5, test_board_2) == True


def test_can_move_to5():
    '''Purpose of test: checking invalid diagonal rook move'''
    assert wr2.can_move_to(4, 4, test_board_2) == False


def test_can_move_to6():
    '''Testing our simulated board matches expectations after a
    capture has taken place'''
    move_success = wr2.can_move_to(2, 5, test_board_2)
    assert move_success

    new_board: Board = wr2.move_to(2, 5, test_board_2)
    size, pieces = new_board

    assert size == 6
    assert len(pieces) == 3

    # Checking that a white rook is now at (2,5)
    rook_found = False
    for p in pieces:
        if isinstance(p, Rook) and p.side == True and p.pos_x == 2 and p.pos_y == 5:
            rook_found = True
    assert rook_found

    # Checking that the black rook is no longer on the board
    br2_still_there = False
    for p in pieces:
        if isinstance(p, Rook) and p.side == False and p.pos_x == 2 and p.pos_y == 5:
            br2_still_there = True
    assert not br2_still_there


# Testing Move_to() for the rook class

wr1a = Rook(3,3, True)

def test_move_to1():
    Actual_B = wr1.move_to(3,3, B1)
    Expected_B = (5, [wr1a, wk1, br1, bk1]) 

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_move_to2():
    '''testing that the moved rook captures an enemy rook'''
    wr = Rook(3, 4, True)
    br = Rook(3, 5, False)
    wk = King(1, 1, True)
    bk = King(5, 5, False)

    B = (6, [wr, br, wk, bk])
    result = wr.move_to(3, 5, B)

    assert len(result[1]) == 3
    assert any(p.pos_x == 3 and p.pos_y == 5 and isinstance(p, Rook) and p.side for p in result[1])
    assert all(not (isinstance(p, Rook) and not p.side and p.pos_x == 3 and p.pos_y == 5) for p in result[1])


def test_move_to3():
    '''testing you can move the king to an empty square'''
    wk = King(2, 2, True)
    wr = Rook(1, 1, True)
    bk = King(5, 5, False)

    B = (6, [wk, wr, bk])
    result = wk.move_to(3, 3, B)

    assert any(p.pos_x == 3 and p.pos_y == 3 and isinstance(p, King) and p.side for p in result[1])
    assert all(not (p.pos_x == 2 and p.pos_y == 2 and isinstance(p, King)) for p in result[1])


def test_move_to4():
    '''Testing if we can move our king to capture black king'''
    wk = King(4, 4, True)
    bk = King(5, 5, False)
    B = (6, [wk, bk])

    result = wk.move_to(5, 5, B)

    assert any(isinstance(p, King) and p.pos_x == 5 and p.pos_y == 5 and p.side for p in result[1])
    assert all(not (p.side == False and p.pos_x == 5 and p.pos_y == 5) for p in result[1])


def test_move_to5():
    '''testing the original board has not been modified'''
    wr = Rook(2, 2, True)
    br = Rook(2, 4, False)
    B = (6, [wr, br])

    result = wr.move_to(2, 4, B)

    assert len(B[1]) == 2
    assert any(p.pos_x ==2 and p.pos_y == 2 and p.side for p in B[1])
    assert any(p.pos_x ==2 and p.pos_y == 4 and not p.side for p in B[1])


# Testing the king class

def test_king_can_move_to1():
    '''testing the king can move in any direction 1 square'''
    king = King(3, 3, True)
    board = (6, [king])
    valid_moves = [(2,2), (2,3), (2,4),
                    (3,2), (3,4),
                    (4,2), (4,3), (4,4)]
    for x,y in valid_moves:
        assert king.can_move_to(x, y, board) == True


def test_king_can_move_to2():
    '''Testing if the king cannot move 2 squares'''
    king = King(3, 3, True)
    board = (6, [king])
    assert king.can_move_to(5,5,board) == False


def test_king_can_move_to3():
    '''Testing king blocked by friendly piece'''
    king = King(3,3, True)
    blocker = Rook(4,3,True)
    board = (6, [king,blocker])
    assert king.can_move_to(4,3,board) == False


def test_king_can_move_to4():
    king = King(3, 3, True)
    enemy = Rook(4,4,False)
    board = (6, [king, enemy])
    assert king.can_move_to(4, 4, board) == True

    new_board = king.move_to(4,4,board)
    _, new_pieces = new_board

    for piece in new_pieces:
        assert not (piece.pos_x == 4 and piece.pos_y == 4 and isinstance(piece, Rook) and piece.side == False)

    found_king = False
    for piece in new_pieces:
        if piece.pos_x ==4 and piece.pos_y ==4 and isinstance(piece,King) and piece.side == True:
            found_king = True
    assert found_king


def test_king_can_move_to5():
    king = King(3, 3, True)
    enemy_rook = Rook(5, 5, False)
    board = (6, [king, enemy_rook])
    assert king.can_move_to(5, 5, board) == False


# Testing King.Move_to()

def test_king_move_to1():
    king = King(2, 2, True)
    board = (6, [king])
    result = king.move_to(3, 3, board)
    assert any(isinstance(p, King) and p.pos_x == 3 and p.pos_y == 3 for p in result[1])


def test_king_move_to2():
    wk = King(2, 2, True)
    br = Rook(3, 3, False)
    board = (6, [wk, br])
    result = wk.move_to(3, 3, board)
    assert all(not (p.pos_x == 3 and p.pos_y == 3 and isinstance(p, Rook)) for p in result[1])


def test_king_move_to3():
    wk = King(3, 3, True)
    br = Rook(4, 4, False)
    board = (6, [wk, br])
    new_board = wk.move_to(4, 4, board)
    size, pieces = new_board
    assert not any(isinstance(p, Rook) and p.pos_x == 4 and p.pos_y == 4 for p in pieces)
    assert any(isinstance(p, King) and p.side and p.pos_x == 4 and p.pos_y == 4 for p in pieces)

def test_king_move_to4():
    wk = King(5, 5, True)
    board = (6, [wk])
    new_board = wk.move_to(6, 6, board)
    _, pieces = new_board
    assert any(isinstance(p, King) and p.side and p.pos_x == 6 and p.pos_y == 6 for p in pieces)


def test_king_move_to5():
    wk = King(2, 2, True)
    board = (6, [wk])
    new_board = wk.move_to(3, 3, board)
    _, pieces = new_board
    assert any(isinstance(p, King) and p.side and p.pos_x == 3 and p.pos_y == 3 for p in pieces)
    assert all(not (p.pos_x == 2 and p.pos_y == 2 and isinstance(p, King)) for p in pieces)


# Adding Tests for is_check()

def test_is_check1():
    B2 = (5, [wr1a, wk1, br1, bk1])
    assert is_check(False, B2) == True


def test_is_check2():
    '''Checkes if white king is in check from a black rook'''
    wk = King(3, 3, True)
    br = Rook(3, 1, False)
    board = (6, [wk, br])
    assert is_check(True, board) == True


def test_is_check3():
    '''Checkes if black king in check horizontally'''
    bk = King(5,5,False)
    wr = Rook(1, 5, True)
    board = (6, [bk, wr])
    assert is_check(False, board) == True


def test_is_check4():
    '''Testing is check when there is a piece in the way'''
    wk = King(3, 3, True)
    br = Rook(3, 1, False)
    wr = Rook(3, 2, True)
    board = (6, [wk, br, wr])
    assert is_check(True, board) == False

def test_is_check5():
    '''Testing a rook doesnt check diagonally'''
    wk = King(4, 4, True)
    br = Rook(1, 1, False)
    board = (6, [wk, br])
    assert is_check(True, board) == False

# Tests for is_checkmate()

def test_is_checkmate1():
    B3 = (5, [wr1a, wk1, br1, bk1, Rook(3,4, True), Rook(3,2,True)])
    assert is_checkmate(False, B3) == True


def test_is_checkmate2():
    '''Situation where king is checkmate by 2 rooks'''
    wk = King(1,1,True)
    br1 = Rook(1,3,False)
    br2 = Rook(3,1,False)
    wr = Rook(2,2,True)
    bk = King(6,6,False)
    board = (6, [wk, br1, br2, wr, bk])
    assert is_checkmate(True, board) == True


def test_is_checkmate3():
    '''Situation where king is in check but there is an escape'''
    wk = King(2, 2, True)
    br = Rook(2, 5, False)
    bk = King(6, 6, False)
    board = (6, [wk,br,bk])
    assert is_checkmate(True, board) == False


def test_is_checkmate4():
    '''Situation where king is checkmate in a corner by rooks'''
    bk = King(6, 6, False)
    wr1 = Rook(6,4, True)
    wr2 = Rook(4,6, True)
    wr3 = Rook(5,4,True)
    wk = King(1, 1, True)
    board = (6, [bk, wr1, wr2, wr3, wk])
    assert is_checkmate(False, board) == True


def test_is_checkmate5():
    '''Situation where king is in check but can take the attacker'''
    bk = King(5, 5, False)
    wr = Rook(4, 5, True)
    wk = King(1, 1, True)
    board = (6, [bk, wr, wk])
    assert is_checkmate(False, board) == False


def test_is_checkmate6():
    '''king is not already in check, but a rook is near'''
    wk = King(2, 2, True)
    br = Rook(4, 2, False)
    bk = King(6, 6, False)
    board = (6, [wk, br, bk])

    assert is_checkmate(True, board) == False


# Test is_stalemate():

def test_is_stalemate1():
    '''Testing a stalement where the king is trapped but not in check'''
    wk = King(1, 1, True)
    br1 = Rook(2, 3, False)
    br2 = Rook(3, 2, False)
    bk = King(6, 6, False)
    board = (6, [wk, br1, br2, bk])
    assert is_stalemate(True, board) == True


def test_is_stalemate2():
    '''Testing when the king is in check so cannot be stalemate'''
    wk = King(2, 2, True)
    br = Rook(2, 5, False)
    board = (6, [wk, br])
    assert is_stalemate(True, board) == False


def test_is_stalemate3():
    '''Testing when the king has a move it can make'''
    wk = King(2, 2, True)
    br = Rook(2, 5, False)
    board = (6, [wk, br])
    assert is_stalemate(True, board) == False


def test_is_stalemate4():
    '''king surrounded by own pieces and no check but pieces can move'''
    wk = King(3, 3, True)
    wr1 = Rook(2,2,True)
    wr2 = Rook(2,3,True)
    wr3 = Rook(2,4,True)
    wr4 = Rook(3,2,True)
    wr5 = Rook(3,4,True)
    wr6 = Rook(4,2,True)
    wr7 = Rook(4,3,True)
    wr8 = Rook(4,4,True)
    bk = King(6,6,False)
    board = (6, [wk,wr1, wr2, wr3, wr4, wr5, wr6, wr7, wr8, bk])
    assert is_stalemate(True, board) == False


def test_is_stalemate5():
    '''King is in corner but not a stalemate'''
    bk = King(6,6,False)
    wr1 = Rook(5,4,True)
    wr2 = Rook(4,5, True)
    wk = King(1, 1, True)
    board = (6, [bk, wr1, wr2, wk])
    assert is_stalemate(False, board) == True


# Test conf2unicode()

def test_conf2unicode1():
    '''testing a single white king'''
    board = (3, [King(2, 2, True)])
    result = conf2unicode(board)
    expected_config = "\u2001\u2001\u2001\n\u2001\u2654\u2001\n\u2001\u2001\u2001"
    assert result == expected_config


def test_conf2unicode2():
    '''testing white rook and black king'''
    board = (4, [Rook(1, 4, True), King(4, 1, False)])
    result = conf2unicode(board)
    expected_config = "\u2656\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u2001\n\u2001\u2001\u2001\u265A"
    assert result == expected_config


def test_conf2unicode3():
    '''testing a fully empty board'''
    board = (3, [])
    result = conf2unicode(board)
    expected_config = "\u2001\u2001\u2001\n\u2001\u2001\u2001\n\u2001\u2001\u2001"
    assert result == expected_config


def test_conf2unicode4():
    '''testing white and black piece in same row'''
    board = (3, [Rook(1, 3, True), Rook(3, 3, False)])
    result = conf2unicode(board)
    expected_config = "\u2656\u2001\u265C\n\u2001\u2001\u2001\n\u2001\u2001\u2001"
    assert result == expected_config


def test_conf2unicode5():
    '''testing a full board'''
    board = (2, [King(1, 2, True), Rook(2, 2, True), King(1, 1, False), Rook(2, 1, False)])
    result = conf2unicode(board)
    expected_config = "\u2654\u2656\n\u265A\u265C"
    assert result == expected_config


# Testing Read Board function

def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    B1 = (5, [King(2,3,False), Rook(5,3,False), King(3,5,True), Rook(4,4, True), Rook(3,1, True)])
    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_read_board2():
    content = '''6
    Kc2, Rd3
    Ke4, Ra1'''

    with open("test_board.txt", "w") as f:
        f.write(content)

    B = read_board("test_board.txt")
    assert B[0] == 6

    B_expected = (6, [King(3, 2, True), Rook(4, 3, True), King(5, 4, False), Rook(1, 1, False)])

    for piece in B[1]:
        found = False
        for piece1 in B_expected[1]:
            if (piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1)):
                    found = True
        assert found

    for piece1 in B_expected[1]:
        found = False 
        for piece in B[1]:
            if (piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1)):
                    found = True
        assert found


def test_read_board3():
    content = '''5
    Kc2, Rd3
    Ra1'''
    with open("test_read_board3.txt", "w") as f:
        f.write(content)
    
    with pytest.raises(IOError):
        read_board("test_read_board3.txt")


def test_read_board4():
    content = '''5
    Kc2, Rc2
    Kd4'''

    with open("test_read_board4.txt", "w") as f:
        f.write(content)

    with pytest.raises(IOError):
        read_board("test_read_board4")

def test_read_board5():
    B = read_board("valid_board.txt")
    assert B[0] == 8

    B_expected = (8, [King(1, 1, True), Rook(2, 2, True), Rook(3, 3, True), King(8, 8, False), Rook(7, 7, False), Rook(6, 6, False)])

    for piece in B_expected[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B_expected[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B_expected[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_read_board6():
    content = '''5
    Kf2
    Kd4'''

    with open("test_read_board6.txt", "w") as f:
        f.write(content)

    with pytest.raises(IOError):
        read_board("test_read_board6.txt")
