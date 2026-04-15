"""Main file."""
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def healh_check():
    return {'message': 'sersice is avaible'}


if __name__ == '__main__':
    uvicorn.run(app)