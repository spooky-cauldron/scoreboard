import logging
from uuid import uuid4

import redis
from flask import Flask

from middleware import body
from schema import PostScoreboardBody, PostScoreboardResponse

app = Flask('scoreboard')

log = logging.getLogger()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.get('/scoreboard/<board_id>')
def get_board_info(board_id: str):
    return r.hgetall(f'board:{board_id}:info')


@app.get('/scoreboard/<board_id>/data')
def get_board_data(board_id: str):
    return r.hgetall(f'board:{board_id}:data')


@app.get('/scoreboard/<board_id>/data/<team>')
def get_board_team_score(board_id: str, team: str):
    return r.hget(f'board:{board_id}:data', team)


@app.post('/scoreboard')
@body(PostScoreboardBody)
def post_board(body: PostScoreboardBody):
    board_id = str(uuid4())
    board_info = {'name': body.name}
    board_data = {team: 0 for team in body.teams}
    r.hset(f'board:{board_id}:info', mapping=board_info)
    r.hset(f'board:{board_id}:data', mapping=board_data)
    response = PostScoreboardResponse(id=board_id, **body.model_dump())
    return response.model_dump()


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
