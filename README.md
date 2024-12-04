# exersise-wordle-like-puzzle

## Overview

This project is a Wordle-like puzzle game implemented using FastAPI. It allows users to guess words and provides feedback on the accuracy of their guesses. The application is designed to handle daily puzzles and random word challenges.

## Features

- **Word Segmentation**: Splits input text into words, filters out numeric values, and stores unique words in the database.
- **Daily Puzzle**: Retrieves a word for the daily puzzle based on the specified size.
- **Random Word Challenge**: Allows users to guess against a random word of a specified size and seed.
- **Word Guessing Feedback**: Provides feedback on each character of the guessed word, indicating if it's correct, present, or absent.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/caohoangphuctd97/exersise-wordle-like-puzzle.git
   cd exersise-wordle-like-puzzle
   ```

2. **Install dependencies** using Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   poetry install
   ```

3. **Set up the database**:
   - Ensure you have a PostgreSQL database running.
   - Configure your database credentials in the `.env` file.

4. **Run database migrations**:
   ```bash
   echo $PWD #Example return: /Users/phuccao/Projects/exersise-wordle-like-puzzle
   export PYTHONPATH={current project path}:app
   #Example: export PYTHONPATH=/Users/phuccao/Projects/exersise-wordle-like-puzzle:app
   alembic upgrade head
   ```

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation**:
   - Open your browser and navigate to `http://localhost:8000/docs` to explore the API endpoints.

## API Endpoints

- **POST /wordseg**: Segments input text into words and stores them in the database.
- **GET /random**: Guess against a random word.
- **GET /daily**: Guess against the daily puzzle.

## Build docker image
```bash
docker-compose -f deployments/docker-compose.yml up -d
```

## Configuration

- The application uses environment variables for configuration. Ensure you have a `.env` file with the necessary database credentials.

## Dependencies

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- PostgreSQL

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
