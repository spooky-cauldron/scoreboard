import logging

import redis
from flask import Flask
from pydantic import BaseModel, Field

from middleware import body

app = Flask('scoreboard')

log = logging.getLogger()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class PostScoreboardBody(BaseModel):
    name: str = Field(min_length=1, max_length=1024)
    teams: list[str] = Field(min_length=1, max_length=1024)


@app.get('/scoreboard')
def get_board_info():
    return r.hgetall('board:info')


@app.get('/scoreboard/data')
def get_board_data():
    return r.hgetall('board:data')


@app.post('/scoreboard')
@body(PostScoreboardBody)
def post_board(body: PostScoreboardBody):
    board_info = {'name': body.name}
    board_data = {team: 0 for team in body.teams}
    r.hset('board:info', mapping=board_info)
    r.hset('board:data', mapping=board_data)
    return body.model_dump()


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
