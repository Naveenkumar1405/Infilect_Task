
---

# Chess Move Calculator API

The Chess Move Calculator API is a FastAPI-based service designed to calculate safe moves for chess pieces on a board. It supports calculating moves for knights, rooks, bishops, and queens, taking into consideration the current state of the board to determine which moves are safe from capture.

## Features

- Calculate valid moves for Knights, Rooks, Bishops, and Queens.
- Filter moves based on safety, excluding those that would result in immediate capture.
- Support for capturing opponent pieces if such moves are deemed safe.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn (for running the server)

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Naveenkumar1405/Infilect_Task.git
cd infilect
```

2. **Install dependencies:**

```bash
pip install fastapi uvicorn pydantic
```

3. **Run the server:**

```bash
uvicorn main:app --reload
```

This command starts the server on `localhost` with port `8000` and enables live reloading for development.

## Usage

The API provides endpoints for each chess piece type (Knight, Rook, Bishop, Queen) at `/chess/<slug>`, where `<slug>` is replaced by the name of the piece you are calculating moves for (e.g., `/chess/knight`).

### Request Format

- **Method:** POST
- **URL:** `http://localhost:8000/chess/queen`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "positions": {
    "Queen": "H1",
    "Bishop": "B7",
    "Rook": "H8",
    "Knight": "F2"
  }
}
```

### Response

The response will contain a list of safe moves for the specified piece:

```json
{
  "safe_moves": [
    "G1",
    "F1",
    ...
  ]
}
```

### Example

Calculating safe moves for a Queen at position H1 with other pieces on the board:

```bash
curl -X 'POST' \
  'http://localhost:8000/chess/queen' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "positions": {
    "Queen": "H1",
    "Bishop": "B7",
    "Rook": "H8",
    "Knight":"F2"
  }
}'
```

## Development

This API is developed with FastAPI. For further development, refer to the FastAPI documentation to understand routing, request handling, and response formatting.

## Contribution

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

[MIT License](LICENSE)

---