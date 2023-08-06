from fastapi import FastAPI
from RandomMath.RandomMathOperations import RandomMath

app = FastAPI()
math = RandomMath()


@app.get("/")
async def root():
    return {"message": "Vamos fazer cálculos aleatórios"}


@app.get("/math/sum/{number}")
async def random_sum(number: int = 0):
    return {"message": math.random_sum(number)}
