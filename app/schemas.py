from pydantic import BaseModel

class WordsegReq(BaseModel):
    text: str
