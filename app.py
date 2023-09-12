import logging
import os
from uuid import uuid4

from flask import Flask
from redis import Redis

from middleware import body
from schema import (
    PatchTeamScoreBody,
    PatchTeamScoreResponse,
    PostScoreboardBody,
    PostScoreboardResponse,
)

app = Flask('scoreboard')
log = logging.getLogger()
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', '6379'))
redis_client = Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True
)


@app.get('/scoreboard/<board_id>')
def get_board_info(board_id: str):
    return redis_client.hgetall(f'board:{board_id}:info')


@app.get('/scoreboard/<board_id>/data')
def get_board_data(board_id: str):
    return redis_client.hgetall(f'board:{board_id}:data')


@app.get('/scoreboard/<board_id>/data/<team>')
def get_board_team_score(board_id: str, team: str):
    return redis_client.hget(f'board:{board_id}:data', team)


@app.patch('/scoreboard/<board_id>/data/<team>')
@body(PatchTeamScoreBody)
def patch_board_team_score(body: PatchTeamScoreBody, board_id: str, team: str):
    total_score = redis_client.hincrby(
        f'board:{board_id}:data',
        team,
        body.amount,
    )
    return PatchTeamScoreResponse(score=total_score).model_dump()


@app.post('/scoreboard')
@body(PostScoreboardBody)
def post_board(body: PostScoreboardBody):
    board_id = str(uuid4())
    board_info = {'name': body.name}
    board_data = {team: 0 for team in body.teams}
    redis_client.hset(f'board:{board_id}:info', mapping=board_info)
    redis_client.hset(f'board:{board_id}:data', mapping=board_data)
    response = PostScoreboardResponse(id=board_id, **body.model_dump())
    return response.model_dump()


if __name__ == '__main__':
    app_host = os.getenv('APP_HOST', 'localhost')
    app_port = int(os.getenv('APP_PORT', '8080'))
    app.run(host=app_host, port=app_port)
