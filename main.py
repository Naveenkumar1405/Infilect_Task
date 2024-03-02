import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(docs_url='/')

class ChessPositionRequest(BaseModel):
    positions: Dict[str, str]

def get_line_moves(start, directions):
    moves = []
    board = "ABCDEFGH"
    start = start.upper()
    row, col = board.index(start[0]), int(start[1]) - 1
    for dr, dc in directions:
        for i in range(1, 8):
            new_row, new_col = row + dr * i, col + dc * i
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                moves.append(board[new_row] + str(new_col + 1))
            else:
                break
    return moves

def get_knight_moves(position):
    position = position.upper()
    moves = []
    board = "ABCDEFGH"
    row, col = board.index(position[0]), int(position[1]) - 1
    directions = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            moves.append(board[new_row] + str(new_col + 1))
    return moves

def get_rook_moves(position):
    return get_line_moves(position, [(0, 1), (0, -1), (1, 0), (-1, 0)])

def get_bishop_moves(position):
    return get_line_moves(position, [(1, 1), (1, -1), (-1, -1), (-1, 1)])

def get_queen_moves(position):
    return get_line_moves(position, [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)])

def is_move_threatened_by_piece(piece_type, piece_position, target_position):
    board = "ABCDEFGH"
    piece_row, piece_col = board.index(piece_position[0]), int(piece_position[1]) - 1
    target_row, target_col = board.index(target_position[0]), int(target_position[1]) - 1

    if piece_type in ["Rook", "Queen"]:
        if piece_row == target_row or piece_col == target_col:
            return True
    if piece_type in ["Bishop", "Queen"]:
        if abs(target_row - piece_row) == abs(target_col - piece_col):
            return True
    if piece_type == "Knight":
        if (abs(target_row - piece_row) == 2 and abs(target_col - piece_col) == 1) or \
           (abs(target_row - piece_row) == 1 and abs(target_col - piece_col) == 2):
            return True
    return False

def can_capture_opponent(target_position: str, positions: Dict[str, str], exclude_piece: str) -> bool:
    for piece, pos in positions.items():
        if piece != exclude_piece and pos == target_position:
            return True
    return False

def is_move_safe(target_position: str, positions: Dict[str, str], moving_piece: str) -> bool:
    for piece, pos in positions.items():
        if piece != moving_piece:
            piece_type = piece.split()[0]
            if is_move_threatened_by_piece(piece_type, pos, target_position):
                return False
    return True

def is_move_safe_after_capture(target_position: str, positions: Dict[str, str], moving_piece: str) -> bool:
    return True

@app.post("/chess/rook")
async def calculate_rook_moves(request: ChessPositionRequest):
    return calculate_piece_moves("rook", request)

@app.post("/chess/knight")
async def calculate_knight_moves(request: ChessPositionRequest):
    return calculate_piece_moves("knight", request)

@app.post("/chess/bishop")
async def calculate_bishop_moves(request: ChessPositionRequest):
    return calculate_piece_moves("bishop", request)

@app.post("/chess/queen")
async def calculate_queen_moves(request: ChessPositionRequest):
    return calculate_piece_moves("queen", request)

def calculate_piece_moves(piece_name: str, request: ChessPositionRequest) -> Dict[str, list]:
    piece_name_capitalized = piece_name.capitalize()
    positions = request.positions
    piece_position = positions.get(piece_name_capitalized, None)

    if not piece_position:
        raise HTTPException(status_code=400, detail=f"{piece_name_capitalized} position not provided")

    try:
        valid_moves = []
        if piece_name.lower() == "knight":
            valid_moves = get_knight_moves(piece_position)
        elif piece_name.lower() == "rook":
            valid_moves = get_rook_moves(piece_position)
        elif piece_name.lower() == "bishop":
            valid_moves = get_bishop_moves(piece_position)
        elif piece_name.lower() == "queen":
            valid_moves = get_queen_moves(piece_position)

        safe_moves = []
        for move in valid_moves:
            if is_move_safe(move, positions, piece_name_capitalized) or can_capture_opponent(move, positions, piece_name_capitalized):
                if is_move_safe_after_capture(move, positions, piece_name_capitalized):
                    safe_moves.append(move)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"valid_moves": safe_moves}

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.1.68", port=8000, reload=True, log_level="debug")