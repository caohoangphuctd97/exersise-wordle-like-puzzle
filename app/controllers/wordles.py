from fastapi.exceptions import HTTPException
from fastapi import status
from datetime import date
from typing import List, Dict
import random

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Wordle


async def wordseg(db: AsyncSession, text: str) -> List[str]:
    """Split a string into words, remove numeric values, and upload words to the database.

    Args:
        db (AsyncSession): database session
        text (str): input text to be processed
    """
    # Split the text into words
    words = text.split()

    # Filter out numeric values
    processed_words = [word for word in words if not word.isnumeric()]
    

    try:
        print("Start store word to db")
        for word in processed_words:
            # Check if the word already exists in the database
            existing_word = await db.execute(select(Wordle).where(Wordle.word == word))
            if existing_word.scalar() is None:
                # Get the current maximum seed for the same length
                current_seed = await db.execute(
                    select(func.max(Wordle.seed)).where(Wordle.length == len(word))
                )
                max_seed = current_seed.scalar() or 0
                # Create a new Wordle object with incremented seed
                wordle_object = Wordle(seed=max_seed + 1, word=word, length=len(word))
                db.add(wordle_object)
                await db.commit()
        print("Store word successfully")
    except Exception as e:
        await db.rollback()
        raise e

async def get_daily_word(db: AsyncSession, size: int) -> Wordle:
    """Retrieve the daily Wordle object from the database based on size.

    Args:
        db (AsyncSession): The database session.
        size (int): The length of the word.

    Returns:
        Wordle: The Wordle object for the current day matching the given size.
    """
    try:
        # Query the database for a Wordle object with the specified size and today's date
        result = await db.execute(
            select(Wordle).where(Wordle.length == size, func.date(Wordle.daily) == date.today())
        )
        wordle = result.scalar_one_or_none()

        if wordle is None:
            result = await db.execute(
                select(Wordle.id).where(Wordle.length == size)
            )
            ids = [row for row in result.scalars()]
            if not ids:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"No Wordle found with size={size}")
            random_id = random.choice(ids)
            random_wordle = await db.get(Wordle, random_id)
            random_wordle.daily = date.today()
            await db.commit()
            return random_wordle

        return wordle

    except Exception as e:
        raise e



async def get_random_wordle(db: AsyncSession, size: int, seed: int, guess: str) -> Wordle:
    """Retrieve a Wordle object from the database based on size and seed.

    Args:
        db (AsyncSession): The database session.
        size (int): The length of the word.
        seed (int): The seed value associated with the word.

    Returns:
        Wordle: The Wordle object matching the given size and seed.
    """
    try:
        # Query the database for a Wordle object with the specified size and seed
        result = await db.execute(
            select(Wordle).where(Wordle.length == size, Wordle.seed == seed)
        )
        wordle = result.scalar_one_or_none()

        if wordle is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Wordle not found with size={size}, seed={seed}")

        res = await check_word_with_guess(wordle.word, guess)
        return res

    except Exception as e:
        raise e


async def check_word_with_guess(word: str, guess: str) -> List[Dict]:
    """Check each character in the word with the guess and return a list indicating matches.

    Args:
        word (str): The word to be guessed.
        guess (str): The guessed word.

    Returns:
        List[str]: A list where each element is 'correct' if the character matches,
                    'present' if the character is in the word but in the wrong position,
                    and 'absent' if the character is not in the word.
    """
    if len(guess) != len(word):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Guess must be the same length as the word")
    
    result = []
    for i, char in enumerate(guess):
        if char == word[i]:
            result.append({
                "slot": i,
                "guess": char,
                "result": "correct"
            })
        elif char in word:
            result.append({
                "slot": i,
                "guess": char,
                "result": "present"
            })
        else:
            result.append({
                "slot": i,
                "guess": char,
                "result": "absent"
            })
    return result
