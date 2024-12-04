from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import wordles
from app.database.depends import create_session


router = APIRouter(
    prefix="",
    tags=["default"]
)

@router.post("/wordseg")
async def wordseg(
    text: str, background_tasks: BackgroundTasks, session: AsyncSession = Depends(create_session)
):
    background_tasks.add_task(wordles.wordseg, session, text)
    output = []
    for word in text.split():
        if not word.isnumeric():
            output.append(f"_{word}")
        else:
            output.append("_{}".format('0' * len(word)))
    return output

@router.get("/random", summary="Guess against a random word")
async def guess_random(
    guess: str, 
    size: int = 5, 
    seed: int = None, 
    session: AsyncSession = Depends(create_session)
):
    data = await wordles.get_random_wordle(session, size, seed, guess)
    return data

@router.get("/daily", summary="Guess against the daily puzzle")
async def guess_daily(
    guess: str, 
    size: int = 5, 
    session: AsyncSession = Depends(create_session)
):
    wordle = await wordles.get_daily_word(session, size)
    result = await wordles.check_word_with_guess(wordle.word, guess)
    return result

@router.get("/word/{word}")
async def guess_word(word: str, guess: str):
    data = await wordles.check_word_with_guess(word, guess)
    return data
